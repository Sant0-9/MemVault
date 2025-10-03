'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthStore } from '@/lib/store'
import api from '@/lib/api'

interface Elder {
  id: number
  name: string
  relationship: string
  birth_date: string | null
  profile_image_url: string | null
  bio: string | null
}

interface DashboardStats {
  total_memories: number
  total_duration_hours: number
  total_elders: number
  memories_this_month: number
}

export default function DashboardPage() {
  const router = useRouter()
  const { user, isAuthenticated, logout } = useAuthStore()
  const [elders, setElders] = useState<Elder[]>([])
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // TEMPORARILY DISABLED AUTH FOR TESTING
    // if (!isAuthenticated()) {
    //   router.push('/login')
    //   return
    // }

    fetchElders()
  }, [isAuthenticated, router])

  const fetchElders = async () => {
    try {
      const [eldersResponse, memoriesResponse] = await Promise.all([
        api.get('/elders/'),
        api.get('/memories/?size=100'),
      ])

      setElders(eldersResponse.data.items)

      const memories = memoriesResponse.data.items
      const totalDuration = memories.reduce(
        (sum: number, m: any) => sum + (m.duration_seconds || 0),
        0
      )
      const now = new Date()
      const thisMonth = memories.filter((m: any) => {
        const created = new Date(m.created_at)
        return (
          created.getMonth() === now.getMonth() &&
          created.getFullYear() === now.getFullYear()
        )
      }).length

      setStats({
        total_memories: memoriesResponse.data.total,
        total_duration_hours: Math.round(totalDuration / 3600),
        total_elders: eldersResponse.data.total,
        memories_this_month: thisMonth,
      })
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  // TEMPORARILY DISABLED AUTH FOR TESTING
  // if (!isAuthenticated()) {
  //   return null
  // }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold">MemoryVault</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground">{user?.name}</span>
            <Button variant="outline" onClick={handleLogout}>
              Logout
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Total Memories</CardDescription>
                <CardTitle className="text-3xl">{stats.total_memories}</CardTitle>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Hours Recorded</CardDescription>
                <CardTitle className="text-3xl">{stats.total_duration_hours}h</CardTitle>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardDescription>Family Members</CardDescription>
                <CardTitle className="text-3xl">{stats.total_elders}</CardTitle>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader className="pb-3">
                <CardDescription>This Month</CardDescription>
                <CardTitle className="text-3xl">+{stats.memories_this_month}</CardTitle>
              </CardHeader>
            </Card>
          </div>
        )}

        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">Quick Actions</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button asChild variant="outline" size="lg" className="h-auto py-4">
              <Link href="/dashboard/elders/new">
                <div className="text-center">
                  <div className="text-2xl mb-2">👴</div>
                  <div className="font-semibold">Add Elder</div>
                </div>
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="h-auto py-4">
              <Link href="/dashboard/memories">
                <div className="text-center">
                  <div className="text-2xl mb-2">🎵</div>
                  <div className="font-semibold">Browse Memories</div>
                </div>
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg" className="h-auto py-4">
              <Link href={elders[0] ? `/dashboard/elders/${elders[0].id}/interview` : '#'}>
                <div className="text-center">
                  <div className="text-2xl mb-2">🎤</div>
                  <div className="font-semibold">Start Interview</div>
                </div>
              </Link>
            </Button>
          </div>
        </div>

        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold">Family Members</h2>
            <p className="text-muted-foreground mt-1">
              Manage and preserve memories of your loved ones
            </p>
          </div>
          <Button asChild>
            <Link href="/dashboard/elders/new">Add Elder</Link>
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Loading...</p>
          </div>
        ) : elders.length === 0 ? (
          <Card>
            <CardHeader>
              <CardTitle>No family members yet</CardTitle>
              <CardDescription>
                Get started by adding your first family member to begin preserving their memories
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild>
                <Link href="/dashboard/elders/new">Add Your First Elder</Link>
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {elders.map((elder) => (
              <Card key={elder.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center text-2xl font-bold">
                      {elder.name.charAt(0)}
                    </div>
                    <div>
                      <CardTitle>{elder.name}</CardTitle>
                      <CardDescription>{elder.relationship}</CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {elder.bio && (
                    <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
                      {elder.bio}
                    </p>
                  )}
                  <div className="flex gap-2">
                    <Button asChild variant="outline" className="flex-1">
                      <Link href={`/dashboard/elders/${elder.id}`}>View</Link>
                    </Button>
                    <Button asChild className="flex-1">
                      <Link href={`/dashboard/elders/${elder.id}/interview`}>
                        Start Interview
                      </Link>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
