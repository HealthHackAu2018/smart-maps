<?php
namespace App\Controller;

use Symfony\Component\HttpFoundation\Response;
use Spatie\PdfToText\Pdf;

class DefaultController
{
    public function index()
    {
        //$number = random_int(0, 100);

        $identifiers = array(
            'Collected:' => ' ',
            'Received:' => ' ',
            'Animal ID:' => ' ',
            'Case ID:' => ' ',
            'Reported:' => ' '
        );
        $testValues = array(
            'RBC' => 3,
            'HAEMOGLOBIN' => 3,
            'HAEMATOCRIT' => 3,
            'MCV' => 3,
            'MCH' => 3,
            'MCHC' => 3,
            'PLATELETS' => 1,
            'PLATELET COUNT' => 3,
            'WBC' => 3,
            'NEUTROPHILS%' => 2,
            'NEUTROPHILS' => 3,
            'LYMPHOCYTES%' => 2,
            'LYMPHOCYTES' => 3,
            'MONOCYTES%' => 2,
            'MONOCYTES' => 3,
            'EOSINOPHILS%' => 2,
            'EOSINOPHILS' => 3,
            'BASOPHILS%' => 2,
            'BASOPHILS' => 3,
            'PROTEIN PLASMA' => 3,
            'FIBRINOGEN' => 3,
            'PLASMA APPEARANCE' => 1,
            'BLOOD SMEAR EXAMINATION' => 1,
        );
        //return new Response(
        //    '<html><body>Lucky number: '.$number.'</body></html>'
        //);        
        $rawText = Pdf::getText('B1705_2000560947.pdf');
        $startOfTable = substr($rawText, strpos($rawText, 'EXAMINATION') + 11);
        $rawText = str_replace("\n", ' ', $rawText); // remove new lines
        $rawText = str_replace("\r", ' ', $rawText); // remove carriage returns
        //echo $rawText;
        $returnValues = array();
        
        

        foreach ($identifiers as $K => $D) {
            $start = strpos($rawText, $K);
           // var_dump($start);
           // var_dump(substr($rawText, $start + strlen($K) + 1));
          //  echo "<HR>";
            $end = strpos(substr($rawText, $start + strlen($K) + 1), $D);
          //  var_dump($end);
          //  echo "<HR>";
            $thisValue = substr($rawText, $start + strlen($K), $end + 2);
          //  var_dump($thisValue);
            $returnValues[$K] = $thisValue;
        }

        //var_dump($returnValues);
        //$result = $this->pdf2text ('B1705_2000560947.pdf');
        //echo $result;

        $counter = 1;
        $startOfTable = str_replace("\n", '', $startOfTable); // remove new lines
        $startOfTable = trim(str_replace("\r", '', $startOfTable)); // remove carriage returns
        foreach ($testValues as $K => $D) {
            $hasNumberic = preg_match('/[0-9]/', $startOfTable, $matches);
            //var_dump($startOfTable);
            //var_dump('    '.$startOfTable);
            // /var_dump($matches);die;
            if ($D == 1) {
                $end = strpos($startOfTable, ' ');
                //var_dump($startOfTable); die;
                //var_dump($end);
                $thisValue = substr($startOfTable, 0, $end+1);
            } else {
                $start = (int)$matches[0];
               // if ($counter == 2){
        var_dump($startOfTable);
               var_dump(substr($startOfTable, $start + strlen($K) + 1));
                echo "<HR>";
               // die;
             //   }
                $end = strpos(substr($startOfTable, $start), ' ');
                //var_dump($end);
                //echo "<HR>";
                
                $thisValue = substr($startOfTable, $start-1, $end+1);
                //var_dump($thisValue); die;

                // Now process the spaces after this value
                $startOfTable = trim(substr($startOfTable, $start + $end));
            
            
                for ($i = 1; $i <= $D; $i++) {
                    echo "<hr>";
                    var_dump($startOfTable);
                    echo "<hr>";
            // var_dump($startOfTable);
            // echo "<HR>";
                //  echo $i;
                    if ($i == 3) {
                        $end = strpos($startOfTable, ')') ;
                        
                        echo $i;var_dump($end);
                    $startOfTable = trim(substr($startOfTable, $end));
                    echo "<hr>";
                    var_dump($startOfTable);
                    echo "<hr>";
                    } else {
                        $end = strpos($startOfTable, ' ');
                        
                        echo $i;var_dump($end);
                    $startOfTable = trim(substr($startOfTable, $end -1));
                        echo "<hr>";
                        var_dump($startOfTable);
                        echo "<hr>";
                    }
                    echo $i;
                    var_dump($end);
                    if ($end > 1){
                    }
                }
            }
            
           // var_dump($startOfTable);
            $returnValues[$K] = $thisValue;
            $counter++;
        }

        return new Response(json_encode($returnValues));
    }

}
