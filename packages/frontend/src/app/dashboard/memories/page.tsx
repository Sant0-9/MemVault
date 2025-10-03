'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import api from '@/lib/api'

interface Memory {
  id: number
  elder_id: number
  title: string
  transcription: string
  summary: string
  category: string
  emotional_tone: string
  era: string
  audio_url: string
  audio_cid: string
  duration_seconds: number
  play_count: number
  created_at: string
}

export default function MemoriesPage() {
  const router = useRouter()
  const [memories, setMemories] = useState<Memory[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  useEffect(() => {
    loadMemories()
  }, [page, selectedCategory])

  const loadMemories = async () => {
    try {
      setLoading(true)
      const params: any = { page, size: 12 }
      if (selectedCategory) params.category = selectedCategory
      if (searchQuery) params.search = searchQuery

      const response = await api.get('/memories/', { params })
      setMemories(response.data.items)
      setTotalPages(response.data.pages)
    } catch (error) {
      console.error('Failed to load memories:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setPage(1)
    loadMemories()
  }

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const categories = [
    'all',
    'childhood',
    'education',
    'career',
    'family',
    'relationships',
    'travel',
    'achievement',
    'challenge',
    'tradition',
    'wisdom',
  ]

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold">Memory Library</h1>
            <p className="text-muted-foreground mt-2">
              Explore and listen to preserved memories
            </p>
          </div>
          <Link href="/dashboard">
            <Button variant="outline">Back to Dashboard</Button>
          </Link>
        </div>

        <div className="mb-6 space-y-4">
          <form onSubmit={handleSearch} className="flex gap-4">
            <Input
              type="text"
              placeholder="Search memories..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1"
            />
            <Button type="submit">Search</Button>
          </form>

          <div className="flex gap-2 flex-wrap">
            {categories.map((category) => (
              <Button
                key={category}
                variant={selectedCategory === category ? 'default' : 'outline'}
                size="sm"
                onClick={() => {
                  setSelectedCategory(category === 'all' ? '' : category)
                  setPage(1)
                }}
              >
                {category.charAt(0).toUpperCase() + category.slice(1)}
              </Button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Loading memories...</p>
          </div>
        ) : memories.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground mb-4">No memories found</p>
            <Link href="/dashboard">
              <Button>Add Your First Memory</Button>
            </Link>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {memories.map((memory) => (
                <Card
                  key={memory.id}
                  className="p-6 hover:shadow-lg transition-shadow cursor-pointer"
                  onClick={() => router.push(`/dashboard/memories/${memory.id}`)}
                >
                  <div className="space-y-3">
                    <div>
                      <h3 className="font-semibold text-lg line-clamp-2">
                        {memory.title || 'Untitled Memory'}
                      </h3>
                      {memory.era && (
                        <p className="text-sm text-muted-foreground">{memory.era}</p>
                      )}
                    </div>

                    {memory.summary && (
                      <p className="text-sm text-muted-foreground line-clamp-3">
                        {memory.summary}
                      </p>
                    )}

                    <div className="flex items-center gap-2 flex-wrap">
                      {memory.category && (
                        <span className="px-2 py-1 bg-primary/10 text-primary text-xs rounded">
                          {memory.category}
                        </span>
                      )}
                      {memory.emotional_tone && (
                        <span className="px-2 py-1 bg-secondary text-secondary-foreground text-xs rounded">
                          {memory.emotional_tone}
                        </span>
                      )}
                    </div>

                    <div className="flex items-center justify-between text-sm text-muted-foreground">
                      <span>{memory.duration_seconds ? formatDuration(memory.duration_seconds) : '—'}</span>
                      <span>{memory.play_count} plays</span>
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            {totalPages > 1 && (
              <div className="flex justify-center gap-2">
                <Button
                  variant="outline"
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                >
                  Previous
                </Button>
                <span className="px-4 py-2 text-sm">
                  Page {page} of {totalPages}
                </span>
                <Button
                  variant="outline"
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                >
                  Next
                </Button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
