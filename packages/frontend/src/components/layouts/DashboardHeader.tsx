'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/lib/store'
import { Home, Search, User, LogOut } from 'lucide-react'

export default function DashboardHeader() {
  const pathname = usePathname()
  const { user, logout } = useAuthStore()

  const handleLogout = () => {
    logout()
    window.location.href = '/'
  }

  const isActive = (path: string) => {
    return pathname.startsWith(path)
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-6">
            <Link href="/dashboard" className="flex items-center gap-2">
              <span className="text-2xl font-bold">MemoryVault</span>
            </Link>

            <nav className="hidden md:flex items-center gap-1">
              <Link href="/dashboard">
                <Button
                  variant={isActive('/dashboard') && pathname === '/dashboard' ? 'secondary' : 'ghost'}
                  size="sm"
                  className="gap-2"
                >
                  <Home className="h-4 w-4" />
                  Dashboard
                </Button>
              </Link>

              <Link href="/dashboard/search">
                <Button
                  variant={isActive('/dashboard/search') ? 'secondary' : 'ghost'}
                  size="sm"
                  className="gap-2"
                >
                  <Search className="h-4 w-4" />
                  Search
                </Button>
              </Link>

              <Link href="/dashboard/memories">
                <Button
                  variant={isActive('/dashboard/memories') ? 'secondary' : 'ghost'}
                  size="sm"
                  className="gap-2"
                >
                  Memories
                </Button>
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-3">
            {user?.name && (
              <div className="hidden sm:flex items-center gap-2 text-sm text-muted-foreground">
                <User className="h-4 w-4" />
                <span>{user.name}</span>
              </div>
            )}

            <Button variant="ghost" size="sm" onClick={handleLogout} className="gap-2">
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
