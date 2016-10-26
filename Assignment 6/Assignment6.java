    /*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
//package weka;


import weka.core.Instance;
import weka.core.Instances;
import weka.core.Utils;
//import weka.core.converters.CSVLoader;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import weka.core.converters.ArffSaver;
import weka.core.converters.CSVLoader;
import java.io.File;
import weka.clusterers.SimpleKMeans; 
/**
 *
 * @author manofsteel
 */
public class Weka {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws Exception
    {
 
    // To load CSV dataset 
    CSVLoader loader = new CSVLoader();
    loader.setSource(new File("/home/manofsteel/bank-data.csv"));
    Instances data = loader.getDataSet();
    String Options="-init 0 -max-candidates 100 -periodic-pruning 10000 -min-density 2.0 -t1 -1.25 -t2 -1.0 -N 10 -A \"weka.core.EuclideanDistance -R first-last\" -I 500 -num-slots 1 -S 10"; 
     
    // SimpleKMeans class is used to create a class object, which will further perform clustering on the dataset.  
    SimpleKMeans kmean= new SimpleKMeans(); 
    kmean.setOptions(weka.core.Utils.splitOptions(Options)); 
    kmean.buildClusterer(data);     
    System.out.println(kmean.toString()); 

    // Now writing the cluster values on to a file.
    // This will give the writer object an empty file to write to. 
    BufferedWriter writer = new BufferedWriter(new FileWriter("/home/manofsteel/test2.arff"));

    // This method is writing the values from the kmeans in terms of a string.
    writer.write(kmean.toString());
    writer.flush();
    writer.close();    
    // program ends here
    }
    
}
