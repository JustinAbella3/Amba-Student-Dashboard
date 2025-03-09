"use client"

import { Line } from "react-chartjs-2"
import { useEffect, useState } from "react"
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js"
import { useTheme } from "next-themes"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

// Update interface to match API response
interface ProgressData {
  _id: string;
  export_date: string;
  total_mastery_points: number;
  total_perseverance_points: number;
  total_course_challenges_passed: number;
  average_mastery_points: number;
  average_perseverance_points: number;
}

export function TotalPerseveranceChart() {
  const { theme } = useTheme()
  const [chartData, setChartData] = useState<ProgressData[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true)
        setError(null)
        
        const response = await fetch('http://127.0.0.1:8000/api/khan/overall/progress', {
          mode: 'cors',
          headers: {
            'Accept': 'application/json'
          }
        })
        
        if (!response.ok) {
          const errorText = await response.text().catch(() => 'No error details available');
          throw new Error(`HTTP error! Status: ${response.status} - ${response.statusText}. Details: ${errorText}`);
        }
        
        const data = await response.json()
        console.log("API Response (Overall Progress):", data);
        
        if (Array.isArray(data)) {
          setChartData(data)
        } else if (data.data && Array.isArray(data.data)) {
          setChartData(data.data)
        } else {
          throw new Error(`Invalid data format received from API: ${JSON.stringify(data).substring(0, 100)}...`)
        }
      } catch (error) {
        console.error('Error fetching data:', error)
        setError(error instanceof Error ? error.message : 'Failed to load data')
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [])

  if (isLoading) return (
    <Card className="shadow-md h-[400px] flex items-center justify-center">
      <CardContent>
        <div className="text-center">Loading perseverance data...</div>
      </CardContent>
    </Card>
  )
  
  if (error) return (
    <Card className="shadow-md">
      <CardHeader className="bg-slate-50 dark:bg-gray-700">
        <CardTitle>Total Perseverance Progress</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="p-4 text-red-500 border border-red-300 rounded bg-red-50 dark:bg-red-900/20 dark:border-red-800">
          <h3 className="font-semibold mb-2">Error Loading Data</h3>
          <p>{error}</p>
        </div>
      </CardContent>
    </Card>
  )
  
  if (chartData.length === 0) return (
    <Card className="shadow-md h-[400px] flex items-center justify-center">
      <CardContent>
        <div className="text-center">No perseverance data available</div>
      </CardContent>
    </Card>
  )

  // Sort data by date
  const sortedData = [...chartData].sort((a, b) => 
    new Date(a.export_date).getTime() - new Date(b.export_date).getTime()
  );

  const data = {
    labels: sortedData.map(d => new Date(d.export_date).toLocaleDateString()),
    datasets: [
      {
        label: "Total Perseverance Points",
        data: sortedData.map(d => d.total_perseverance_points),
        borderColor: "rgb(153, 102, 255)",
        backgroundColor: "rgba(153, 102, 255, 0.2)",
        tension: 0.1,
      }
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
        labels: {
          color: theme === 'dark' ? '#f3f4f6' : '#374151',
        }
      },
      title: {
        display: false,
      },
      tooltip: {
        backgroundColor: theme === 'dark' ? '#374151' : '#ffffff',
        titleColor: theme === 'dark' ? '#f3f4f6' : '#111827',
        bodyColor: theme === 'dark' ? '#e5e7eb' : '#374151',
        borderColor: theme === 'dark' ? '#4b5563' : '#e5e7eb',
        borderWidth: 1,
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Perseverance Points',
          color: theme === 'dark' ? '#e5e7eb' : '#374151',
        },
        grid: {
          color: theme === 'dark' ? '#374151' : '#e5e7eb',
        },
        ticks: {
          color: theme === 'dark' ? '#e5e7eb' : '#374151',
        }
      },
      x: {
        title: {
          display: true,
          text: 'Date',
          color: theme === 'dark' ? '#e5e7eb' : '#374151',
        },
        grid: {
          color: theme === 'dark' ? '#374151' : '#e5e7eb',
        },
        ticks: {
          maxRotation: 45,
          minRotation: 45,
          color: theme === 'dark' ? '#e5e7eb' : '#374151',
        }
      }
    }
  }

  return (
    <Card className="shadow-md dark:bg-gray-800 dark:text-gray-100 rounded-lg overflow-hidden">
      <CardHeader className="bg-slate-50 dark:bg-gray-700">
        <CardTitle>Total Perseverance Progress</CardTitle>
      </CardHeader>
      <CardContent className="pt-6">
        <div className="h-[300px]">
          <Line options={options} data={data} />
        </div>
      </CardContent>
    </Card>
  )
}