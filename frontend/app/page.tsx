import { StudentMasteryRankings } from "@/app/components/StudentMasteryRankings"
import { StudentPerseveranceRankings } from "@/app/components/StudentPerseveranceRankings"
import { TotalMasteryChart } from "@/app/components/TotalMasteryChart"
import { TotalPerseveranceChart } from "@/app/components/TotalPerseveranceChart"
import { ThemeToggleButton } from "@/app/components/ThemeToggleButton"
import { ThemeDebug } from "@/app/components/ThemeDebug"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col p-6 gap-6 bg-gray-50 dark:bg-gray-900">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold mb-2 text-gray-900 dark:text-white">Khan Academy Dashboard</h1>
        <ThemeToggleButton />
      </div>
      
      {/* Rankings Section */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <StudentMasteryRankings />
        </div>
        <div>
          <StudentPerseveranceRankings />
        </div>
      </section>
      
      {/* Charts Section */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
        <div>
          <TotalMasteryChart />
        </div>
        <div>
          <TotalPerseveranceChart />
        </div>
      </section>
      
      <ThemeDebug />
    </main>
  )
}
