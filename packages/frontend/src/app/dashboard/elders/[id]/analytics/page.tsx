'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import api from '@/lib/api'
import { BarChart, TrendingUp, Heart, Clock, MapPin, Users } from 'lucide-react'

interface AnalyticsData {
  elder_id: number
  elder_name: string
  overview: {
    total_memories: number
    total_duration_seconds: number
    total_duration_formatted: string
    average_duration_seconds: number
    memories_with_audio: number
    memories_with_transcription: number
  }
  timeline_analysis: {
    decades: Array<{ decade: string; count: number }>
    eras: Array<{ era: string; count: number }>
    earliest_memory: string | null
    latest_memory: string | null
    span_years: number
  }
  content_analysis: {
    categories: Array<{ category: string; count: number }>
    total_categories: number
    locations_mentioned: string[]
    total_locations: number
    people_mentioned: string[]
    total_people: number
    top_tags: Array<{ tag: string; count: number }>
  }
  emotional_insights: {
    emotion_distribution: Array<{ emotion: string; count: number; percentage: number }>
    dominant_emotion: string | null
    emotional_diversity: number
  }
  engagement_metrics: {
    total_plays: number
    total_shares: number
    average_plays_per_memory: number
    most_played_memory: { id: number; title: string; play_count: number } | null
    most_shared_memory: { id: number; title: string; share_count: number } | null
  }
  quality_metrics: {
    average_transcription_confidence: number
    average_audio_quality: number
    memories_with_high_quality_transcription: number
    memories_with_low_quality_transcription: number
    memories_needing_review: number
  }
}

export default function AnalyticsPage() {
  const params = useParams()
  const elderId = parseInt(params.id as string)
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [elderId])

  const fetchAnalytics = async () => {
    try {
      const response = await api.get(`/analytics/elders/${elderId}/analytics`)
      setAnalytics(response.data)
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <p className="text-muted-foreground">Loading analytics...</p>
      </div>
    )
  }

  if (!analytics) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <p className="text-muted-foreground">No analytics data available</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen gradient-bg">
      <header className="border-b border-primary/20 bg-card/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <Link
            href={`/dashboard/elders/${elderId}`}
            className="text-sm text-muted-foreground hover:text-foreground"
          >
            ← Back to Elder Profile
          </Link>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Analytics & Insights</h1>
          <p className="text-muted-foreground">
            Comprehensive analysis for {analytics.elder_name}&apos;s memories
          </p>
        </div>

        <div className="space-y-6">
          {/* Overview Stats */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
              <CardHeader className="pb-3">
                <CardDescription>Total Memories</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">{analytics.overview.total_memories}</div>
              </CardContent>
            </Card>

            <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
              <CardHeader className="pb-3">
                <CardDescription>Total Duration</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">
                  {analytics.overview.total_duration_formatted}
                </div>
              </CardContent>
            </Card>

            <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
              <CardHeader className="pb-3">
                <CardDescription>With Audio</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">
                  {analytics.overview.memories_with_audio}
                </div>
              </CardContent>
            </Card>

            <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
              <CardHeader className="pb-3">
                <CardDescription>With Transcription</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold">
                  {analytics.overview.memories_with_transcription}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Timeline Analysis */}
          <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Timeline Analysis
              </CardTitle>
              <CardDescription>Life coverage and time span</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold mb-3">Decades Covered</h3>
                  <div className="space-y-2">
                    {analytics.timeline_analysis.decades.map((decade) => (
                      <div key={decade.decade} className="flex items-center justify-between">
                        <span className="text-sm">{decade.decade}</span>
                        <div className="flex items-center gap-2">
                          <div className="w-32 bg-muted rounded-full h-2">
                            <div
                              className="bg-primary h-2 rounded-full"
                              style={{
                                width: `${
                                  (decade.count /
                                    Math.max(
                                      ...analytics.timeline_analysis.decades.map((d) => d.count)
                                    )) *
                                  100
                                }%`,
                              }}
                            />
                          </div>
                          <span className="text-sm font-medium w-8 text-right">
                            {decade.count}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold mb-3">Time Span</h3>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Earliest Memory:</span>
                      <span className="font-medium">
                        {analytics.timeline_analysis.earliest_memory
                          ? new Date(
                              analytics.timeline_analysis.earliest_memory
                            ).getFullYear()
                          : 'N/A'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Latest Memory:</span>
                      <span className="font-medium">
                        {analytics.timeline_analysis.latest_memory
                          ? new Date(analytics.timeline_analysis.latest_memory).getFullYear()
                          : 'N/A'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Span:</span>
                      <span className="font-medium">
                        {analytics.timeline_analysis.span_years} years
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Content & Emotional Insights */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart className="h-5 w-5" />
                  Content Distribution
                </CardTitle>
                <CardDescription>Memory categories and themes</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analytics.content_analysis.categories.slice(0, 5).map((category) => (
                    <div key={category.category} className="flex items-center justify-between">
                      <span className="text-sm">{category.category}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-24 bg-muted rounded-full h-2">
                          <div
                            className="bg-primary h-2 rounded-full"
                            style={{
                              width: `${
                                (category.count / analytics.overview.total_memories) * 100
                              }%`,
                            }}
                          />
                        </div>
                        <span className="text-sm font-medium w-8 text-right">
                          {category.count}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Heart className="h-5 w-5" />
                  Emotional Insights
                </CardTitle>
                <CardDescription>Emotional tone distribution</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {analytics.emotional_insights.emotion_distribution.map((emotion) => (
                    <div key={emotion.emotion} className="flex items-center justify-between">
                      <span className="text-sm capitalize">{emotion.emotion}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-24 bg-muted rounded-full h-2">
                          <div
                            className="bg-primary h-2 rounded-full"
                            style={{ width: `${emotion.percentage}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium w-12 text-right">
                          {emotion.percentage}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
                {analytics.emotional_insights.dominant_emotion && (
                  <div className="mt-4 p-3 bg-muted rounded-lg">
                    <p className="text-sm text-muted-foreground">Dominant Emotion</p>
                    <p className="font-semibold capitalize">
                      {analytics.emotional_insights.dominant_emotion}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* People & Locations */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  People Mentioned
                </CardTitle>
                <CardDescription>
                  {analytics.content_analysis.total_people} people across memories
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {analytics.content_analysis.people_mentioned.slice(0, 15).map((person) => (
                    <span
                      key={person}
                      className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm"
                    >
                      {person}
                    </span>
                  ))}
                  {analytics.content_analysis.people_mentioned.length > 15 && (
                    <span className="px-3 py-1 bg-muted text-muted-foreground rounded-full text-sm">
                      +{analytics.content_analysis.people_mentioned.length - 15} more
                    </span>
                  )}
                </div>
              </CardContent>
            </Card>

            <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MapPin className="h-5 w-5" />
                  Locations Mentioned
                </CardTitle>
                <CardDescription>
                  {analytics.content_analysis.total_locations} locations across memories
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {analytics.content_analysis.locations_mentioned.slice(0, 10).map((location) => (
                    <span
                      key={location}
                      className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm"
                    >
                      {location}
                    </span>
                  ))}
                  {analytics.content_analysis.locations_mentioned.length > 10 && (
                    <span className="px-3 py-1 bg-muted text-muted-foreground rounded-full text-sm">
                      +{analytics.content_analysis.locations_mentioned.length - 10} more
                    </span>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Quality Metrics */}
          <Card className="card-hover border-primary/20 bg-card/50 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Quality Metrics
              </CardTitle>
              <CardDescription>Transcription and audio quality analysis</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">
                    Avg. Transcription Confidence
                  </p>
                  <p className="text-2xl font-bold">
                    {Math.round(analytics.quality_metrics.average_transcription_confidence * 100)}%
                  </p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Avg. Audio Quality</p>
                  <p className="text-2xl font-bold">
                    {Math.round(analytics.quality_metrics.average_audio_quality * 100)}%
                  </p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Memories Needing Review</p>
                  <p className="text-2xl font-bold">
                    {analytics.quality_metrics.memories_needing_review}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
