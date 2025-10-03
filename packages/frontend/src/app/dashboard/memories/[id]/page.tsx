'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
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
  people_mentioned: string[]
  location: string
  created_at: string
}

export default function MemoryDetailPage() {
  const router = useRouter()
  const params = useParams()
  const memoryId = params.id as string
  const [memory, setMemory] = useState<Memory | null>(null)
  const [loading, setLoading] = useState(true)
  const [playing, setPlaying] = useState(false)
  const audioRef = useRef<HTMLAudioElement>(null)

  const loadMemory = useCallback(async () => {
    try {
      const response = await api.get(`/memories/${memoryId}`)
      setMemory(response.data)
    } catch (error) {
      console.error('Failed to load memory:', error)
    } finally {
      setLoading(false)
    }
  }, [memoryId])

  useEffect(() => {
    loadMemory()
  }, [loadMemory])

  const togglePlayPause = () => {
    if (audioRef.current) {
      if (playing) {
        audioRef.current.pause()
      } else {
        audioRef.current.play()
      }
      setPlaying(!playing)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-muted-foreground">Loading memory...</p>
      </div>
    )
  }

  if (!memory) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground mb-4">Memory not found</p>
          <Link href="/dashboard/memories">
            <Button>Back to Memories</Button>
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-6">
          <Link href="/dashboard/memories">
            <Button variant="outline">← Back to Library</Button>
          </Link>
        </div>

        <Card className="p-8">
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold mb-2">{memory.title}</h1>
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                {memory.era && <span>{memory.era}</span>}
                <span>•</span>
                <span>Played {memory.play_count} times</span>
                <span>•</span>
                <span>{formatDate(memory.created_at)}</span>
              </div>
            </div>

            {memory.audio_url && (
              <div className="bg-muted p-6 rounded-lg">
                <div className="flex items-center gap-4">
                  <Button
                    size="lg"
                    onClick={togglePlayPause}
                    className="w-16 h-16 rounded-full"
                  >
                    {playing ? '⏸' : '▶'}
                  </Button>
                  <div className="flex-1">
                    <p className="text-sm text-muted-foreground mb-1">Audio Recording</p>
                    <p className="text-lg font-medium">
                      {memory.duration_seconds
                        ? formatDuration(memory.duration_seconds)
                        : 'Unknown duration'}
                    </p>
                  </div>
                </div>
                <audio
                  ref={audioRef}
                  src={memory.audio_url}
                  onEnded={() => setPlaying(false)}
                  onPause={() => setPlaying(false)}
                  onPlay={() => setPlaying(true)}
                  className="w-full mt-4"
                  controls
                />
              </div>
            )}

            <div className="flex gap-2 flex-wrap">
              {memory.category && (
                <span className="px-3 py-1 bg-primary/10 text-primary rounded-full">
                  {memory.category}
                </span>
              )}
              {memory.emotional_tone && (
                <span className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full">
                  {memory.emotional_tone}
                </span>
              )}
            </div>

            {memory.summary && (
              <div>
                <h2 className="text-xl font-semibold mb-2">Summary</h2>
                <p className="text-muted-foreground">{memory.summary}</p>
              </div>
            )}

            <div>
              <h2 className="text-xl font-semibold mb-2">Full Transcription</h2>
              <div className="prose prose-slate max-w-none">
                <p className="whitespace-pre-wrap">{memory.transcription}</p>
              </div>
            </div>

            {(memory.people_mentioned?.length > 0 || memory.location) && (
              <div className="border-t pt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
                {memory.people_mentioned && memory.people_mentioned.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-2">People Mentioned</h3>
                    <div className="flex flex-wrap gap-2">
                      {memory.people_mentioned.map((person, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-1 bg-muted text-sm rounded"
                        >
                          {person}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                {memory.location && (
                  <div>
                    <h3 className="font-semibold mb-2">Location</h3>
                    <p className="text-muted-foreground">{memory.location}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  )
}
