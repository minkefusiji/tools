$MachineListFile = "machielist.txt"
$DMClientPath = "D:\app\APTools.ap_06_25_10_8_5005_3622\"
$ProcessingNumber = 0

if ([System.IO.File]::Exists($MachineListFile)) {
    $FileContent = (Get-Content -Path $MachineListFile)
    foreach($line in $FileContent)
    {
        if((([string]$line).Length -gt 0))
        {
            $ProcessingNumber += 1
            $items =  $line -split ","
            $Command = $DMClientPath + "dmclient.exe -f -c ""SetMachineStatus -t F -m -s " + $items[0] + """"
            echo "Command:" $Command
            echo "Result:" `$Command

            if ($ProcessingNumber -ge 10)
            {
                Start-Sleep -s 3600
                $ProcessingNumber = 0   
            }
        }
    }
} else {
    echo ($MachineListFile + " doesn't exist")
}