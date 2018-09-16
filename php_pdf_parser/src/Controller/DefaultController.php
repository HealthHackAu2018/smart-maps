<?php
/**
 * Default controller for smart maps
 *
 * PHP version 7.2
 *
 * @category   HealthHack
 * @package    SmartMaks
 * @author     Wilma Karsdorp <w.karsdorp@gmail.com>
 * @version    1
 */

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Spatie\PdfToText\Pdf;
use Symfony\Bundle\FrameworkBundle\Controller\Controller;

class DefaultController extends Controller
{
    /**
     * Index
     * 
     * This is where the files can be uploaded
     *
     * @return page
     **/
    public function index()
    {
        return $this->render('uploads.html.twig', array());
    }

    /**
     * Process the PDF documents
     *
     * translate uploaded pdf documents to json or csv
     *
     * @param Request $request Get or post request
     * @param bool  $csv Export to csv, otherwise json
     * @return csv output or json
     **/
    public function processData(Request $request, $csv = true)
    {
        // pdf identifiers
        $identifiers = array(
            'Animal ID:' => ' Unique',
            'Case ID:' => ' ',
            'Collected:' => ' ',
            'Received:' => ' ',
            'Reported:' => ' '
        );
        // the test values in the document
        $testValues = array(
            'RBC' => ')',
            'HAEMOGLOBIN' => ')',
            'HAEMATOCRIT' => ')',
            'RETICULOCYTE %' => ')',
            'RETICULOCYTE ABS' => '/L',
            'MCV' => ')',
            'MCH' => ')',
            'MCHC' => ')',
            'PLATELETS' => ' ',
            'PLATELET COUNT' => ')',
            'WBC' => ')',
            'NEUTROPHILS%' => '%',
            'NEUTROPHILS' => ')',
            'LYMPHOCYTES%' => '%',
            'LYMPHOCYTES' => ')',
            'MONOCYTES%' => '%',
            'MONOCYTES' => ')',
            'EOSINOPHILS%' => '%',
            'EOSINOPHILS' => ')',
            'BASOPHILS%' => '%',
            'BASOPHILS' => ')',
            'NUCLEATED RBCS' => 'wbc',
            'PROTEIN PLASMA' => ')',
            'FIBRINOGEN' => ')',
            'PLASMA APPEARANCE' => 'text',
            'BLOOD SMEAR EXAMINATION' => 'end',
        );
        
        for ($i = 0; $i < count($_FILES['files-conf']['name']); $i++) {
            if (is_uploaded_file($_FILES['files-conf']["tmp_name"][$i])) {
                $returnValues[$_FILES['files-conf']['name'][$i]] = $this->getContent(
                    $_FILES['files-conf']["tmp_name"][$i],
                    $identifiers,
                    $testValues,
                    $csv
                );
            }
        }
        if ($csv) {
            return $this->render('csv.html.twig', array('identifiers' => $identifiers, 'testValues' =>$testValues, 'results' => $returnValues));
        }
        return new Response(json_encode($returnValues));
    }

    /**
     * Get the content of the PDF
     *
     **/
    private function getContent($fileName, $identifiers, $testValues, $csv = false)
    {
        if ($csv) {
            $returnValues = '';
        } else {
            $returnValues = array();
        }
        $rawText = Pdf::getText($fileName);
        $startOfTable = substr($rawText, strpos($rawText, 'EXAMINATION') + 11);
        $digitalOffset = $this->digitalOffset($startOfTable);
        $startOfTable = substr($startOfTable, $digitalOffset);

        $rawText = substr($rawText, 0, strpos($rawText, 'EXAMINATION'));
        $rawText = str_replace("\n", ' ', $rawText); // remove new lines
        $rawText = str_replace("\r", ' ', $rawText); // remove carriage returns
        
        $isValidFile = true;
        foreach ($identifiers as $K => $D) {
            $start = strpos($rawText, $K);
            $end = strpos(substr($rawText, $start + strlen($K) + 1), $D);
            $thisValue = substr($rawText, $start + strlen($K), $end + 2);
            // Check if this is a valid document for this process. If not, continue
            if ($thisValue == '') {
                $isValidFile = false;
                $thisValue = 'invalid file';
            }
            if ($csv) {
                $returnValues .= $thisValue .',';
            } else {
                $returnValues[$K] = $thisValue;
            }
            if (!$isValidFile) {
                break;
            }
        }

        if (!$isValidFile) {
            return $returnValues;
        }

        $counter = 1;
        $startOfTable = str_replace("\n", '', $startOfTable); // remove new lines
        $startOfTable = trim(str_replace("\r", '', $startOfTable)); // remove carriage returns
        $endOfTable = strpos($startOfTable, 'For tests indicated by a hash');
        $startOfTable = substr($startOfTable, 0, $endOfTable);
        foreach ($testValues as $K => $D) {
            // If this test value is not in the list, do not continue;
            // Blood smear examinition is always on the list, and is the last entry
            if (strpos($rawText, $K) === false && $K != 'BLOOD SMEAR EXAMINATION') {
                if ($csv) {
                    $returnValues .= 'na' .',';
                } else {
                    $returnValues[$K] = 'na';
                }
                $counter++;
                continue;
            }

            $hasNumberic = preg_match('/[0-9]/', $startOfTable, $matches, PREG_OFFSET_CAPTURE);
            $end = strpos($startOfTable, ' ');
           
            if ($D == ' ') {
                $start = 0;
                $endOfRow = (int)$matches[0][1] -2;
                $end = $endOfRow;
            } elseif ($D == 'text') {
                $start = 0;
                $endOfRow = strpos($startOfTable, ' ') - 1;
                $end = strpos($startOfTable, ' ');
            } elseif ($D == 'end') {
                $start = 0;
                $endOfRow = strlen($startOfTable);
                $end = strlen($startOfTable);
            } else {
                $start = (int)$matches[0][1];
                $endOfRow = strpos($startOfTable, $D);
            }
            if ($start == 0) {
                $start = 1;
            }
            $thisValue = substr($startOfTable, $start-1, $end+1);

            $startOfTable = trim(substr($startOfTable, $start + $endOfRow + 1));
            if ($csv) {
                $returnValues .= $thisValue .',';
            } else {
                    $returnValues[$K] = $thisValue;
            }
            $counter++;
        }
        return $returnValues;
    }

    /**
     * Get the positon of the first digital
     *
     **/
    private function digitalOffset($text)
    {
        preg_match('/^\D*(?=\d)/', $text, $m);
        return isset($m[0]) ? strlen($m[0]) : false;
    }
}
