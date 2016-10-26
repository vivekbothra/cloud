

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
public class WeekByWeekMapReduce 
{// Main class.


 public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, DoubleWritable> 
   {
      //Map class starts here.
      public void map(LongWritable key, Text value, OutputCollector<Text, DoubleWritable> output, Reporter reporter) throws IOException 
      {

          String line = value.toString();
          String[] tokenizer = line.split(",");
       
          String[] date = tokenizer[0].split("T");
          Double d = new Double("0.0");
          
          SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");  //MM denotes the month of the year mm gives the minutes.
          
          Date dt = null; 
          try
          {
            dt = formatter.parse(date[0]); 
          }
          catch(ParseException p)
          {
            p.printStackTrace();
          }
          Calendar cal = Calendar.getInstance();
          cal.setTime(dt);
          int week = cal.get(Calendar.WEEK_OF_YEAR); 
          String wk_num = "Week"+week;
          
          
          double var = d.parseDouble(tokenizer[4]);
      
          
          
          if((var<3.0)&&(var>0.5))
          {
              output.collect(new Text(wk_num),new DoubleWritable(var));
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
         JobConf conf = new JobConf(WeekByWeekMapReduce.class);
         conf.setJobName("weekbyweekmapreduce");
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