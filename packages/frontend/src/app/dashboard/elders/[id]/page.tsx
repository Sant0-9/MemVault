'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import api from '@/lib/api'

interface Elder {
  id: number
  name: string
  relationship: string
  birth_date: string | null
  bio: string | null
}

interface Memory {
  id: number
  title: string
  category: string | null
  created_at: string
}

export default function ElderDetailPage() {
  const params = useParams()
  const elderId = params.id as string
  const [elder, setElder] = useState<Elder | null>(null)
  const [memories, setMemories] = useState<Memory[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [elderId])

  const fetchData = async () => {
    try {
      const [elderResponse, memoriesResponse] = await Promise.all([
        api.get(`/elders/${elderId}`),
        api.get(`/memories/?elder_id=${elderId}`),
      ])

      setElder(elderResponse.data)
      setMemories(memoriesResponse.data.items)
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-muted-foreground">Loading...</p>
      </div>
    )
  }

  if (!elder) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-muted-foreground">Elder not found</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <Link href="/dashboard" className="text-sm text-muted-foreground hover:text-foreground">
            ← Back to Dashboard
          </Link>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-3xl">{elder.name}</CardTitle>
                  <CardDescription className="text-lg mt-1">
                    {elder.relationship}
                  </CardDescription>
                </div>
                <Button asChild>
                  <Link href={`/dashboard/elders/${elderId}/interview`}>
                    Start Interview
                  </Link>
                </Button>
              </div>
            </CardHeader>
            {elder.bio && (
              <CardContent>
                <p className="text-muted-foreground">{elder.bio}</p>
              </CardContent>
            )}
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Memories ({memories.length})</CardTitle>
              <CardDescription>
                Recorded memories and stories
              </CardDescription>
            </CardHeader>
            <CardContent>
              {memories.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-muted-foreground mb-4">
                    No memories recorded yet
                  </p>
                  <Button asChild>
                    <Link href={`/dashboard/elders/${elderId}/interview`}>
                      Record First Memory
                    </Link>
                  </Button>
                </div>
              ) : (
                <div className="space-y-4">
                  {memories.map((memory) => (
                    <div
                      key={memory.id}
                      className="border rounded-lg p-4 hover:bg-accent transition-colors"
                    >
                      <h3 className="font-medium">{memory.title}</h3>
                      {memory.category && (
                        <span className="inline-block mt-2 px-2 py-1 text-xs rounded-full bg-primary/10 text-primary">
                          {memory.category}
                        </span>
                      )}
                      <p className="text-xs text-muted-foreground mt-2">
                        {new Date(memory.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
