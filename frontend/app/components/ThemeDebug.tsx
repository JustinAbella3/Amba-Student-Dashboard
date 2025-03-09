"use client"

import { useTheme } from "next-themes"
import { useEffect, useState } from "react"

export function ThemeDebug() {
  const { theme, resolvedTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <div className="fixed bottom-4 right-4 bg-white dark:bg-gray-800 p-2 rounded shadow text-xs">
      <div>Theme: {theme}</div>
      <div>Resolved: {resolvedTheme}</div>
    </div>
  )
} 