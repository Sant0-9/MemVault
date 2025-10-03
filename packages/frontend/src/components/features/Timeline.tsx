'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import api from '@/lib/api'
import { Calendar, MapPin, Heart } from 'lucide-react'

interface Memory {
  id: number
  title: string
  category: string | null
  date_of_event: string | null
  summary: string | null
  emotional_tone: string | null
  location: string | null
}

interface TimelinePeriod {
  period: string
  memories: Memory[]
  count: number
}

interface TimelineData {
  elder_id: number
  elder_name: string
  group_by: string
  total_memories: number
  timeline: TimelinePeriod[]
}

interface TimelineStats {
  total_memories: number
  earliest_memory: string | null
  latest_memory: string | null
  decades_covered: string[]
  total_decades: number
  categories: Record<string, number>
  eras: Record<string, number>
  completeness_score: number
}

interface TimelineProps {
  elderId: number
}

export default function Timeline({ elderId }: TimelineProps) {
  const [timelineData, setTimelineData] = useState<TimelineData | null>(null)
  const [stats, setStats] = useState<TimelineStats | null>(null)
  const [groupBy, setGroupBy] = useState<'decade' | 'year' | 'era' | 'category'>('decade')
  const [loading, setLoading] = useState(true)
  const [expandedPeriods, setExpandedPeriods] = useState<Set<string>>(new Set())

  useEffect(() => {
    fetchTimeline()
    fetchStats()
  }, [elderId, groupBy])

  const fetchTimeline = async () => {
    try {
      const response = await api.get(`/timeline/elders/${elderId}/timeline`, {
        params: { group_by: groupBy },
      })
      setTimelineData(response.data)
    } catch (error) {
      console.error('Failed to fetch timeline:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await api.get(`/timeline/elders/${elderId}/timeline/stats`)
      setStats(response.data)
    } catch (error) {
      console.error('Failed to fetch timeline stats:', error)
    }
  }

  const togglePeriod = (period: string) => {
    const newExpanded = new Set(expandedPeriods)
    if (newExpanded.has(period)) {
      newExpanded.delete(period)
    } else {
      newExpanded.add(period)
    }
    setExpandedPeriods(newExpanded)
  }

  const getEmotionColor = (tone: string | null) => {
    const colors: Record<string, string> = {
      joyful: 'text-yellow-600',
      nostalgic: 'text-blue-600',
      reflective: 'text-purple-600',
      proud: 'text-green-600',
      bittersweet: 'text-orange-600',
      humorous: 'text-pink-600',
      serious: 'text-gray-600',
      sad: 'text-red-600',
    }
    return tone ? colors[tone.toLowerCase()] || 'text-gray-500' : 'text-gray-500'
  }

  if (loading) {
    return (
      <Card>
        <CardContent className="py-8">
          <p className="text-center text-muted-foreground">Loading timeline...</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-6">
      {stats && (
        <Card>
          <CardHeader>
            <CardTitle>Timeline Overview</CardTitle>
            <CardDescription>Life story completeness and statistics</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Total Memories</p>
                <p className="text-2xl font-bold">{stats.total_memories}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Decades Covered</p>
                <p className="text-2xl font-bold">{stats.total_decades}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Completeness</p>
                <p className="text-2xl font-bold">{Math.round(stats.completeness_score)}%</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Time Span</p>
                <p className="text-sm font-medium">
                  {stats.earliest_memory
                    ? new Date(stats.earliest_memory).getFullYear()
                    : '—'}
                  {' - '}
                  {stats.latest_memory ? new Date(stats.latest_memory).getFullYear() : '—'}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Life Timeline</CardTitle>
              <CardDescription>
                Explore memories through {timelineData?.elder_name}&apos;s life
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button
                variant={groupBy === 'decade' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setGroupBy('decade')}
              >
                Decades
              </Button>
              <Button
                variant={groupBy === 'year' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setGroupBy('year')}
              >
                Years
              </Button>
              <Button
                variant={groupBy === 'era' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setGroupBy('era')}
              >
                Life Stages
              </Button>
              <Button
                variant={groupBy === 'category' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setGroupBy('category')}
              >
                Categories
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {!timelineData || timelineData.timeline.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground">No memories to display</p>
            </div>
          ) : (
            <div className="space-y-4">
              {timelineData.timeline.map((period) => (
                <div key={period.period} className="border rounded-lg overflow-hidden">
                  <button
                    onClick={() => togglePeriod(period.period)}
                    className="w-full px-4 py-3 bg-muted hover:bg-muted/80 transition-colors text-left flex items-center justify-between"
                  >
                    <div>
                      <h3 className="font-semibold text-lg">{period.period}</h3>
                      <p className="text-sm text-muted-foreground">
                        {period.count} {period.count === 1 ? 'memory' : 'memories'}
                      </p>
                    </div>
                    <div className="text-muted-foreground">
                      {expandedPeriods.has(period.period) ? '−' : '+'}
                    </div>
                  </button>

                  {expandedPeriods.has(period.period) && (
                    <div className="p-4 space-y-3">
                      {period.memories.map((memory) => (
                        <div
                          key={memory.id}
                          className="border-l-4 border-primary/30 pl-4 py-2 hover:border-primary transition-colors"
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex-1">
                              <h4 className="font-medium">{memory.title}</h4>
                              {memory.summary && (
                                <p className="text-sm text-muted-foreground mt-1">
                                  {memory.summary}
                                </p>
                              )}
                              <div className="flex flex-wrap gap-3 mt-2 text-xs text-muted-foreground">
                                {memory.date_of_event && (
                                  <span className="flex items-center gap-1">
                                    <Calendar className="h-3 w-3" />
                                    {new Date(memory.date_of_event).toLocaleDateString()}
                                  </span>
                                )}
                                {memory.location && (
                                  <span className="flex items-center gap-1">
                                    <MapPin className="h-3 w-3" />
                                    {memory.location}
                                  </span>
                                )}
                                {memory.emotional_tone && (
                                  <span
                                    className={`flex items-center gap-1 ${getEmotionColor(
                                      memory.emotional_tone
                                    )}`}
                                  >
                                    <Heart className="h-3 w-3" />
                                    {memory.emotional_tone}
                                  </span>
                                )}
                              </div>
                            </div>
                            {memory.category && (
                              <span className="px-2 py-1 text-xs rounded-full bg-primary/10 text-primary whitespace-nowrap">
                                {memory.category}
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
