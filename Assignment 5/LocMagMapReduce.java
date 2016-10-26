
import java.io.IOException;
import java.util.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;
import java.text.SimpleDateFormat;
import java.text.ParseException;
  

//Program starts here.
public class LocMagMapReduce 
{// Main class.
 public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, DoubleWritable> 
   {
      //Map class starts here.
      public void map(LongWritable key, Text value, OutputCollector<Text, DoubleWritable> output, Reporter reporter) throws IOException 
      {

          String line = value.toString();
          String[] tokenizer = line.split(",");
          Double latitude = Double.parseDouble(tokenizer[1]);
          Double longitude = Double.parseDouble(tokenizer[2]);
          String lat_long;
          Double d = new Double("0.0");
          double var = d.parseDouble(tokenizer[4]);
          if((latitude<20.0)&&(latitude>10.0))
          {
             if((longitude>-125.0)&&(longitude>-130.0))
             {
                lat_long = "Lat20/10_Long-125/-130";
                output.collect(new Text(lat_long),new DoubleWritable(var));
             }
              
          }
           if((latitude<30.0)&&(latitude>20.0))
          {
             if((longitude>-120.0)&&(longitude>-125.0))
             {
                lat_long = "Lat30/20_Long-120/-125";
                output.collect(new Text(lat_long),new DoubleWritable(var));
             }
              
          }
           if((latitude<40.0)&&(latitude>30.0))
          {
             if((longitude>-115.0)&&(longitude>-120.0))
             {
                lat_long = "Lat40/30_Long-115/-120";
                output.collect(new Text(lat_long),new DoubleWritable(var));
             }
              
          }
           if((latitude<50.0)&&(latitude>40.0))
          {
             if((longitude>-110.0)&&(longitude>-115.0))
             {
                lat_long = "Lat50/40_Long-110/-115";
                output.collect(new Text(lat_long),new DoubleWritable(var));
             }
              
          }
           

          System.err.println("Leaving the map method");
          
         
      } 
    }

     public static class Reduce extends MapReduceBase implements Reducer<Text, DoubleWritable, Text, DoubleWritable> 
     {
         public void reduce(Text key, Iterator<DoubleWritable> values, OutputCollector<Text, DoubleWritable> output, Reporter reporter) throws IOException 
         {
         
       
            double avg = 0.0;
            int count = 0;
            while(values.hasNext())
            {
              avg += values.next().get();
              count++;
            }
            avg = (avg / count);
            //count = 0;
            output.collect(key, new DoubleWritable(avg));

         }
     }
      public static void main(String[] args) throws Exception 
     {
         long start = System.currentTimeMillis();           
         JobConf conf = new JobConf(LocMagMapReduce.class);
         conf.setJobName("locmagmapreduce");
         conf.setNumMapTasks(1);
             conf.setNumReduceTasks(1);
         conf.setOutputKeyClass(Text.class);
         conf.setOutputValueClass(DoubleWritable.class);
    
         conf.setMapperClass(Map.class);
         conf.setCombinerClass(Reduce.class);
         conf.setReducerClass(Reduce.class);
    
         conf.setInputFormat(TextInputFormat.class);
         conf.setOutputFormat(TextOutputFormat.class);
    
         FileInputFormat.setInputPaths(conf, new Path(args[0]));
         FileOutputFormat.setOutputPath(conf, new Path(args[1]));
    
         JobClient.runJob(conf);
         long end = System.currentTimeMillis();
         long diff = end -start; 
         System.err.println("Time is "+diff);
     }
      
  }