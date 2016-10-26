



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
public class DayByDayMapReduce 
{// Main class.

public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, DoubleWritable> 
   {
      //Map class starts here.
      public void map(LongWritable key, Text value, OutputCollector<Text, DoubleWritable> output, Reporter reporter) throws IOException 
      {

          String line = value.toString();
          String[] tokenizer = line.split(",");
      //  System.err.println("The file has been split using , ");
          String[] date = tokenizer[0].split("T");
          Double d = new Double("0.0");

          double var = Math.round(d.parseDouble(tokenizer[4]));
      //  System.out.println("Rounded num"+var);
          
          if((var<3.0)&&(var>0.5))
          {
              output.collect(new Text(date[0]),new DoubleWritable(var));
          }
         

          System.err.println("Leaving the map method");
      } 
    }

     public static class Reduce extends MapReduceBase implements Reducer<Text, DoubleWritable, Text, DoubleWritable> 
     {
         public void reduce(Text key, Iterator<DoubleWritable> values, OutputCollector<Text, DoubleWritable> output, Reporter reporter) throws IOException 
         {
         
      //      System.err.println(" In the reduce method ");

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
         JobConf conf = new JobConf(DayByDayMapReduce.class);
         conf.setJobName("daybydaymapreduce");
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
