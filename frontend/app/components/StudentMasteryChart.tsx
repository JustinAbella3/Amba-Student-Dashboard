"use client"

import { useEffect, useState } from "react"
import { CartesianGrid, Line, LineChart, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "../../node_modules/recharts"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

interface MasteryData {
  date: string;
  [student: string]: string | number;
}

// Generate a unique color for each student
const getStudentColor = (index: number) => {
  const colors = [
    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", 
    "#FF9F40", "#8AC926", "#1982C4", "#6A4C93", "#FF595E"
  ];
  return colors[index % colors.length];
};

export function StudentMasteryChart() {
  const [data, setData] = useState<MasteryData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/khan/all-students/mastery-progress');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!data.length) return <div>No data available</div>;

  // Get all student names from the first data point
  const studentNames = Object.keys(data[0]).filter(key => key !== 'date');

  return (
    <Card>
      <CardHeader>
        <CardTitle>Student Mastery Progress</CardTitle>
        <CardDescription>Daily mastery points for all students</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            {studentNames.map((student, index) => (
              <Line 
                key={student}
                type="monotone"
                dataKey={student}
                stroke={getStudentColor(index)}
                activeDot={{ r: 8 }}
                name={student}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
      <CardFooter>
        <div className="text-sm text-muted-foreground">
          Showing daily mastery points earned by each student
        </div>
      </CardFooter>
    </Card>
  );
} 