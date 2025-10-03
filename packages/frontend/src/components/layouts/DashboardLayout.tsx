'use client'

import { ReactNode } from 'react'
import DashboardHeader from './DashboardHeader'

interface DashboardLayoutProps {
  children: ReactNode
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '4xl' | '6xl' | '7xl' | 'full'
}

const maxWidthClasses = {
  sm: 'max-w-screen-sm',
  md: 'max-w-screen-md',
  lg: 'max-w-screen-lg',
  xl: 'max-w-screen-xl',
  '2xl': 'max-w-screen-2xl',
  '4xl': 'max-w-4xl',
  '6xl': 'max-w-6xl',
  '7xl': 'max-w-7xl',
  full: 'max-w-full',
}

export default function DashboardLayout({ children, maxWidth = '7xl' }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />
      <main className={`container mx-auto px-4 py-8 ${maxWidthClasses[maxWidth]}`}>
        {children}
      </main>
    </div>
  )
}
