$files = [IO.Directory]::GetFiles("c:\Users\es579dx\Desktop\temp DATA\Python_Parser\sample_data\")
foreach($file in $files) 
{     
    $content = get-content -path $file
    $content | out-file $file -encoding BigEndianUnicode   
}
