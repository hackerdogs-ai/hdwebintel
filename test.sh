echo "Starting tests for Web Intelligence WebService"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
host="localhost"
port="5000"
echo
echo $host : $port
echo
echo Line $LINENO
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
cmd="curl "http://$host:$port/webc/api/version""
echo $cmd
echo
$cmd
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO


cmd="curl "http://$host:$port/webc/api/v1.0/webmodel?url=https://www.microsoft.com""
echo $cmd
echo
$cmd

echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO

cmd="curl "http://$host:$port/webc/api/v1.0/domainmodel?url=https://www.logicmonitor.com""
echo $cmd
echo
$cmd
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO

curl -d '{"txt":"One day a close friend asked me a question, “What is the difference between Efficiency and Effectiveness?” Many people use those words interchangeably, but depending on the context you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what a degree means. On the other hand, efficiency is clearly defined as the ratio or output to the input. So, it is a scientific term and is easier to measure. In today’s volatile world, businesses need efficiency and not effectiveness. The success of your business depends upon the efficiency of your customers and employees - nothing more nothing less. "}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/txtmodel

echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo  "http://$host:$port/webc/api/v1.0/findcreditcards"
echo Line $LINENO

curl -d '{"txt":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341 or get in touch with my associate at harold.smith@gmail.com"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/findcreditcards
echo
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
cmd="curl http://$host:$port/webc/api/v1.0/webmodel?url=https://www.paypalobjects.com/en_GB/vhelp/paypalmanager_help/credit_card_numbers.htm"
echo $cmd
echo
$cmd
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "http://$host:$port/webc/api/v1.0/findsensitivedata"
echo Line $LINENO
curl -d '{"txt":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341 or get in touch with my associate at harold.smith@gmail.com"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/findsensitivedata
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"

echo "http://$host:$port/webc/api/v1.0/geodistance"
echo Line $LINENO
curl -d '{"source_lat":"37.6652", "source_long":"-121.8734", "dest_lat":"18.516726", "dest_long":"73.856255"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/geodistance

echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"

echo "http://$host:$port/webc/api/v1.0/geoipdistance"
echo Line $LINENO
curl -d '{"source_ip":"40.112.72.205", "dest_ip":"73.223.111.77"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/geoipdistance

echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "http://$host:$port/webc/api/v1.0/geodomaindistance"
echo Line $LINENO
curl -d '{"source_domain":"www.microsoft.com", "dest_domain":"www.google.com"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/geodomaindistance
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"source_lat":"37.6652", "source_long":"-121.8734", "dest_lat":"18.516726", "dest_long":"73.856255"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/geodistance
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"txt1":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341 or get in touch with my associate at harold.smith@gmail.com", "txt2":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341 or get in touch with my associate at harold.smith@gmail.com"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/similarity/levenshtein
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"txt1":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341 or get in touch with my associate at harold.smith@gmail.com", "txt2":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/similarity/levenshtein
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"txt1":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341 or get in touch with my associate at harold.smith@gmail.com", "txt2":"This is completely different!!!"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/similarity/levenshtein
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"txt1":"Arohi is my name", "txt2":"My name is Tejaswi Redkar"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/similarity/spacy
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"txt1":"This article discusses the helpful features provided by the VS Code Python extension for working with Python environments. An environment in Python is the context in which a Python program runs and consists of an interpreter and any number of installed packages. After you finish this article, youll have a good understanding of", "txt2":"This article discusses the helpful features provided by the VS Code Python extension for working with Python environments. An environment in Python is the context in which a Python program runs and consists of an interpreter and any number of installed packages. After you finish this article, youll have a good understanding of"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/similarity/spacy
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"topn":20, "txt":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341 or get in touch with my associate at harold.smith@gmail.com"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/keyterms/textrank
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl "http://$host:$port/webc/api/v1.0/scan?port=53&host=www.sumologic.com"
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"txt":"This article discusses the helpful features provided by the VS Code Python extension for working with Python environments. An environment in Python is the context in which a Python program runs and consists of an interpreter and any number of installed packages. After you finish this article, youll have a good understanding of"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/lang
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"txt":"ha supervisado y finalizado correspondencia y otros documentos escritos en francés para su presentación al Secretario y al Secretario Adjunto."}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/lang
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl "http://$host:$port/webc/api/v1.0/clearcache"
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl "http://$host:$port/webc/api/v1.0/certificate?d=logicmonitor.com"
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl "http://$host:$port/webc/api/v1.0/sysmetrics"
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"txt1":"This article discusses the helpful features provided by the VS Code Python extension for working with Python environments. An environment in Python is the context in which a Python program runs and consists of an interpreter and any number of installed packages. After you finish this article, youll have a good understanding of", "txt2":"This article discusses the helpful features provided by the VS Code Python extension for working with Python environments. An environment in Python is the context in which a Python program runs and consists of an interpreter and any number of installed packages. After you finish this article, youll have a good understanding of"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/similarity/all
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"topn":20, "txt":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/keyterms/all
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"topn":20, "txt":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/keyterms/all
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl -d '{"topn":20, "txt":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341 or get in touch with my associate at harold.smith@gmail.com"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/keyterms/all
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl "http://$host:$port/webc/api/v1.0/tld?url=microsoft.com"
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl -d '{"topn":20, "txt":"One fe80:0000:0000:0000:0204:61ff:254.157.241.86 day a close fe80:0000:0000:0000:0204:61ff:fe9d:f156 friend fe80:0:0:0:204:61ff:fe9d:f156 asked me 127.0.0.1, 192.168.1.1, 8.8.8.8 a question, “What is the (523)222-8888 ext 527 difference (523)222-8888x623 between @tejaswiredkar Efficiency @dynamicdeploy and Effectiveness?” Many people 1LgqButDNV2rVHe9DATt6WqD8tKZEKvaK2 use those (17.789576, -78.2323) words 1Bow5EMqtDGV5n5xZVgdpR interchangeably, but (17.789576, -78.2323) depending 345L0gicMonitor345 on the context (17.789576, -78.2323) you use, the outcome could be completely different. The definition of effectiveness is about degree to which a desired outcome can be achieved - note that it leaves out what 94583 2665 Paige Way, Dublin, CA 94443 a degree means. On 427-45-9033 the other hand, efficiency is clearly defined as 4222222222222 the 5019717010103742 ratio or 6331101999990016 output to the 76009244561 input. So, it is a scientific term and is easier to abc@abc.ai measure. In today’s support@microsoft.com volatile world, businesses need efficiency and not 5610591081018250 effectiveness. 4012888888881881 The success of 4111111111111111 your business 5105105105105100 depends upon the 378734493671000  efficiency of 371449635398431your customers and employees - 378282246310005 nothing 5555555555554444 more nothing less. John, please get that article on www.linkedin.com to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, 12345678900, 1234567890, +1 234 567 8900, 234-567-8900,1-234-567-8900, 1.234.567.8900, 5678900,567-8900,(123) 456 7890, +41 22 730 5989, (+41) 22 730 5989,+442345678900. You can reach me at (519)-236-2723x341 or get in touch with my associate at harold.smith@gmail.com"}' -H "Content-Type: application/json" -X POST http://$host:$port/webc/api/v1.0/removestopwords
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo 
echo Line $LINENO
curl "http://$host:$port/webc/api/v1.0/tld?url=www.microsoft.com"
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl "http://$host:$port/webc/api/v1.0/tld?url=https://www.microsoft.com"
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl http://$host:$port/webc/api/v1.0/getlang?url=http://maharashtratimes.com
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl http://$host:$port/webc/api/v1.0/getips?domain_name=microsoft.com
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl http://$host:$port/webc/api/v1.0/ipwhois?ip=162.255.119.254
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl http://$host:$port/webc/api/v1.0/getiploc?ip=162.255.119.254
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
curl http://$host:$port/webc/api/v1.0/webmodel?url=https://www.dynamicdeploy.com
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl http://$host:$port/webc/api/v1.0/wlang?url=https://www.microsoft.com/zh-cn
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl http://$host:$port/webc/api/v1.0/wlang?url=https://cn.nytimes.com/
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl http://$host:$port/webc/api/v1.0/wlang?url=https://www.gulfarabic.com/es/
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl -i -H "Content-Type: application/json" -X POST -d '{"txt":"Read a book by tejaswi@outlook.com and write a book by dynamicdeploy@live.com"}' http://$host:$port/webc/api/v1.0/txtmodel

echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl "http://$host:$port/webc/api/v1.0/tld?url=office.microsoft.com"
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo
echo Line $LINENO
curl "http://$host:$port/webc/api/v1.0/tld?url=www.github.io"
echo
echo
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo "********************v*****************************************************"
echo Line $LINENO
echo "Ending tests for Web Intelligence WebService"