"use client"

import { useState, useEffect } from "react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface Student {
  student_name: string;
  total_mastery_points: number;
  total_perseverance_points: number;
  rank_by_mastery: number;
  rank_by_perseverance: number;
}

export function StudentPerseveranceRankings() {
  const [students, setStudents] = useState<Student[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true)
        setError(null)
        const response = await fetch('http://127.0.0.1:8000/api/khan/rankings/current/perseverance', {
          mode: 'cors',
          headers: {
            'Accept': 'application/json'
          }
        })
        
        if (!response.ok) {
          const errorText = await response.text().catch(() => 'No error details available');
          throw new Error(`HTTP error! Status: ${response.status} - ${response.statusText}. Details: ${errorText}`);
        }
        
        // Parse the response as JSON
        const data = await response.json()
        console.log("API Response (Perseverance):", data); // Log the response for debugging
        
        // Check if data is an array (based on your sample data)
        if (Array.isArray(data)) {
          setStudents(data)
        } else if (data.data && Array.isArray(data.data)) {
          // Alternative format if the API returns {success: true, data: [...]}
          setStudents(data.data)
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

  if (isLoading) return <div className="p-4 text-center">Loading student perseverance data...</div>
  if (error) return (
    <div className="p-4 text-red-500 border border-red-300 rounded bg-red-50 dark:bg-red-900/20 dark:border-red-800">
      <h3 className="font-semibold mb-2">Error Loading Data</h3>
      <p>{error}</p>
    </div>
  )
  if (students.length === 0) return <div className="p-4 text-center">No student perseverance data available</div>

  // Sort students by perseverance points in descending order
  const sortedStudents = [...students].sort((a, b) => 
    (b.total_perseverance_points || 0) - (a.total_perseverance_points || 0)
  )

  return (
    <Card className="shadow-md dark:bg-gray-800 dark:text-gray-100 rounded-lg overflow-hidden">
      <CardHeader className="bg-slate-50 dark:bg-gray-700">
        <CardTitle>Student Perseverance Rankings</CardTitle>
      </CardHeader>
      <CardContent className="pt-6">
        <div className="max-h-[400px] overflow-y-auto">
          <Table>
            <TableHeader className="sticky top-0 bg-white dark:bg-gray-800 z-10">
              <TableRow>
                <TableHead className="dark:text-gray-200">Rank</TableHead>
                <TableHead className="dark:text-gray-200">Student Name</TableHead>
                <TableHead className="text-right dark:text-gray-200">Perseverance Points</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedStudents.map((student, index) => (
                <TableRow key={student.student_name || index} className="dark:border-gray-700">
                  <TableCell className="font-medium dark:text-gray-300">
                    {student.rank_by_perseverance || index + 1}
                  </TableCell>
                  <TableCell className="dark:text-gray-300">
                    {student.student_name}
                  </TableCell>
                  <TableCell className="text-right dark:text-gray-300">
                    {typeof student.total_perseverance_points === 'number' 
                      ? student.total_perseverance_points.toLocaleString() 
                      : student.total_perseverance_points}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  )
}