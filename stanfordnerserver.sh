java="/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java"
jar="/Users/bram/Documents/Universiteit/Onderzoeksproject/stanford-ner/stanford-ner.jar"
classifier="/Users/bram/Documents/Universiteit/Onderzoeksproject/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz"
echo "Starting Server..."
# "$java" -Djava.ext.dirs=./lib -cp "$jar" edu.stanford.nlp.ie.NERServer -port 9199 -loadClassifier "$classifier"
"$java" -mx1000m -cp "$jar":lib/* edu.stanford.nlp.ie.NERServer -loadClassifier "$classifier" -port 8080
