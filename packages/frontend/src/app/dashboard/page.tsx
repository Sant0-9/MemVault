'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuthStore } from '@/lib/store'
import api from '@/lib/api'
import DashboardLayout from '@/components/layouts/DashboardLayout'

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
  const { isAuthenticated } = useAuthStore()
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

  // TEMPORARILY DISABLED AUTH FOR TESTING
  // if (!isAuthenticated()) {
  //   return null
  // }

  return (
    <DashboardLayout>
      <div className="relative">
        <div className="mb-10 fade-in-up">
          <h1 className="text-3xl font-semibold tracking-tight text-white mb-2">
            Dashboard
          </h1>
          <p className="text-neutral-400 text-sm">
            Overview of your family memories and stories
          </p>
        </div>

        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-12 fade-in-up" style={{ animationDelay: '0.1s' }}>
            <Card className="stat-card">
              <CardHeader className="pb-2 pt-5">
                <CardDescription className="text-xs font-medium text-neutral-500 mb-1">Total Memories</CardDescription>
                <CardTitle className="text-3xl font-semibold tracking-tight text-white number-shift">{stats.total_memories}</CardTitle>
              </CardHeader>
            </Card>
            <Card className="stat-card">
              <CardHeader className="pb-2 pt-5">
                <CardDescription className="text-xs font-medium text-neutral-500 mb-1">Hours Recorded</CardDescription>
                <CardTitle className="text-3xl font-semibold tracking-tight text-white number-shift">{stats.total_duration_hours}h</CardTitle>
              </CardHeader>
            </Card>
            <Card className="stat-card">
              <CardHeader className="pb-2 pt-5">
                <CardDescription className="text-xs font-medium text-neutral-500 mb-1">Family Members</CardDescription>
                <CardTitle className="text-3xl font-semibold tracking-tight text-white number-shift">{stats.total_elders}</CardTitle>
              </CardHeader>
            </Card>
            <Card className="stat-card">
              <CardHeader className="pb-2 pt-5">
                <CardDescription className="text-xs font-medium text-neutral-500 mb-1">This Month</CardDescription>
                <CardTitle className="text-3xl font-semibold tracking-tight text-white number-shift">+{stats.memories_this_month}</CardTitle>
              </CardHeader>
            </Card>
          </div>
        )}

        <div className="mb-12 fade-in-up" style={{ animationDelay: '0.2s' }}>
          <h2 className="text-xl font-semibold tracking-tight text-white mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
            <Link href="/dashboard/elders/new">
              <Card className="modern-card p-4 cursor-pointer group">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center group-hover:bg-purple-500/20 transition-colors">
                    <svg className="w-5 h-5 text-neutral-400 group-hover:text-purple-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                  </div>
                  <div className="flex-1">
                    <div className="font-medium text-sm text-white">Add Elder</div>
                    <div className="text-xs text-neutral-500">Create profile</div>
                  </div>
                </div>
              </Card>
            </Link>
            <Link href="/dashboard/memories">
              <Card className="modern-card p-4 cursor-pointer group">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center group-hover:bg-purple-500/20 transition-colors">
                    <svg className="w-5 h-5 text-neutral-400 group-hover:text-purple-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                  </div>
                  <div className="flex-1">
                    <div className="font-medium text-sm text-white">Browse Memories</div>
                    <div className="text-xs text-neutral-500">View collection</div>
                  </div>
                </div>
              </Card>
            </Link>
            <Link href="/dashboard/search">
              <Card className="modern-card p-4 cursor-pointer group">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center group-hover:bg-purple-500/20 transition-colors">
                    <svg className="w-5 h-5 text-neutral-400 group-hover:text-purple-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                  </div>
                  <div className="flex-1">
                    <div className="font-medium text-sm text-white">Search</div>
                    <div className="text-xs text-neutral-500">Find memories</div>
                  </div>
                </div>
              </Card>
            </Link>
            <Link href={elders[0] ? `/dashboard/elders/${elders[0].id}/interview` : '#'}>
              <Card className="modern-card p-4 cursor-pointer group">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-purple-500/20 flex items-center justify-center group-hover:bg-purple-500/30 transition-colors">
                    <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" /></svg>
                  </div>
                  <div className="flex-1">
                    <div className="font-medium text-sm text-white">Start Interview</div>
                    <div className="text-xs text-neutral-500">Record now</div>
                  </div>
                </div>
              </Card>
            </Link>
          </div>
        </div>

        <div className="flex items-center justify-between mb-4 fade-in-up" style={{ animationDelay: '0.3s' }}>
          <h2 className="text-xl font-semibold tracking-tight text-white">Family Members</h2>
          <Button asChild size="sm" className="bg-white hover:bg-neutral-200 text-black">
            <Link href="/dashboard/elders/new">Add Elder</Link>
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-neutral-500 text-sm">Loading...</p>
          </div>
        ) : elders.length === 0 ? (
          <Card className="modern-card p-12 text-center fade-in-up" style={{ animationDelay: '0.4s' }}>
            <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-white/5 flex items-center justify-center">
              <svg className="w-8 h-8 text-neutral-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
            </div>
            <h3 className="text-base font-medium text-white mb-2">No family members yet</h3>
            <p className="text-sm text-neutral-400 mb-6 max-w-sm mx-auto">
              Get started by adding your first family member to begin preserving their memories
            </p>
            <Button asChild className="bg-white hover:bg-neutral-200 text-black">
              <Link href="/dashboard/elders/new">Add Your First Elder</Link>
            </Button>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 fade-in-up" style={{ animationDelay: '0.4s' }}>
            {elders.map((elder) => (
              <Card key={elder.id} className="modern-card p-5 group">
                <div className="flex items-start gap-4 mb-4">
                  <div className="w-12 h-12 rounded-xl bg-white/5 flex items-center justify-center text-lg font-semibold text-neutral-300 group-hover:bg-purple-500/20 group-hover:text-purple-400 transition-colors">
                    {elder.name.charAt(0)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-white truncate">{elder.name}</h3>
                    <p className="text-sm text-neutral-400">{elder.relationship}</p>
                  </div>
                </div>
                {elder.bio && (
                  <p className="text-sm text-neutral-400 mb-4 line-clamp-2 leading-relaxed">
                    {elder.bio}
                  </p>
                )}
                <div className="flex gap-2">
                  <Button asChild variant="outline" size="sm" className="flex-1 text-xs border-white/10 hover:bg-white/5">
                    <Link href={`/dashboard/elders/${elder.id}`}>View</Link>
                  </Button>
                  <Button asChild size="sm" className="flex-1 bg-white hover:bg-neutral-200 text-black text-xs">
                    <Link href={`/dashboard/elders/${elder.id}/interview`}>Interview</Link>
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  )
}
