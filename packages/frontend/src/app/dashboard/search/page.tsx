'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import api from '@/lib/api'
import { Search, Filter, Calendar, MapPin, Heart, X } from 'lucide-react'

interface SearchResult {
  id: number
  elder_id: number
  title: string
  summary: string | null
  category: string | null
  era: string | null
  decade: string | null
  emotional_tone: string | null
  location: string | null
  date_of_event: string | null
  created_at: string
}

interface Facet {
  value: string
  count: number
}

interface SearchResponse {
  query: string
  total: number
  page: number
  page_size: number
  total_pages: number
  results: SearchResult[]
  facets: {
    categories: Facet[]
    eras: Facet[]
    decades: Facet[]
    emotional_tones: Facet[]
  }
  filters_applied: Record<string, any>
}

export default function SearchPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '')
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [showFilters, setShowFilters] = useState(false)

  const [filters, setFilters] = useState({
    category: searchParams.get('category') || '',
    era: searchParams.get('era') || '',
    decade: searchParams.get('decade') || '',
    emotional_tone: searchParams.get('emotional_tone') || '',
    location: searchParams.get('location') || '',
  })

  useEffect(() => {
    const q = searchParams.get('q')
    if (q) {
      setSearchQuery(q)
      performSearch(q)
    }
  }, [searchParams])

  const performSearch = async (query: string) => {
    if (!query.trim()) return

    setLoading(true)
    try {
      const params: Record<string, string> = { q: query }

      Object.entries(filters).forEach(([key, value]) => {
        if (value) {
          params[key] = value
        }
      })

      const response = await api.get('/search/search', { params })
      setSearchResults(response.data)
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    const params = new URLSearchParams({ q: searchQuery })
    Object.entries(filters).forEach(([key, value]) => {
      if (value) params.append(key, value)
    })
    router.push(`/dashboard/search?${params.toString()}`)
  }

  const updateFilter = (key: string, value: string) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
  }

  const clearFilter = (key: string) => {
    updateFilter(key, '')
  }

  const clearAllFilters = () => {
    setFilters({
      category: '',
      era: '',
      decade: '',
      emotional_tone: '',
      location: '',
    })
  }

  const getActiveFiltersCount = () => {
    return Object.values(filters).filter(v => v).length
  }

  const getEmotionColor = (tone: string | null) => {
    const colors: Record<string, string> = {
      joyful: 'bg-yellow-100 text-yellow-800',
      nostalgic: 'bg-blue-100 text-blue-800',
      reflective: 'bg-purple-100 text-purple-800',
      proud: 'bg-green-100 text-green-800',
      bittersweet: 'bg-orange-100 text-orange-800',
      humorous: 'bg-pink-100 text-pink-800',
      serious: 'bg-gray-100 text-gray-800',
      sad: 'bg-red-100 text-red-800',
    }
    return tone ? colors[tone.toLowerCase()] || 'bg-gray-100 text-gray-800' : 'bg-gray-100 text-gray-800'
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

      <main className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Search Memories</h1>
          <p className="text-muted-foreground">
            Search across all memories with advanced filters
          </p>
        </div>

        <form onSubmit={handleSearch} className="mb-6">
          <div className="flex gap-2">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                type="text"
                placeholder="Search memories..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button type="submit" disabled={loading}>
              Search
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => setShowFilters(!showFilters)}
            >
              <Filter className="h-4 w-4 mr-2" />
              Filters {getActiveFiltersCount() > 0 && `(${getActiveFiltersCount()})`}
            </Button>
          </div>
        </form>

        {showFilters && searchResults && (
          <Card className="mb-6">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Filters</CardTitle>
                {getActiveFiltersCount() > 0 && (
                  <Button variant="ghost" size="sm" onClick={clearAllFilters}>
                    Clear All
                  </Button>
                )}
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Category</label>
                  <select
                    value={filters.category}
                    onChange={(e) => updateFilter('category', e.target.value)}
                    className="w-full px-3 py-2 border rounded-md"
                  >
                    <option value="">All Categories</option>
                    {searchResults.facets.categories.map((facet) => (
                      <option key={facet.value} value={facet.value}>
                        {facet.value} ({facet.count})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">Era/Life Stage</label>
                  <select
                    value={filters.era}
                    onChange={(e) => updateFilter('era', e.target.value)}
                    className="w-full px-3 py-2 border rounded-md"
                  >
                    <option value="">All Eras</option>
                    {searchResults.facets.eras.map((facet) => (
                      <option key={facet.value} value={facet.value}>
                        {facet.value} ({facet.count})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">Decade</label>
                  <select
                    value={filters.decade}
                    onChange={(e) => updateFilter('decade', e.target.value)}
                    className="w-full px-3 py-2 border rounded-md"
                  >
                    <option value="">All Decades</option>
                    {searchResults.facets.decades.map((facet) => (
                      <option key={facet.value} value={facet.value}>
                        {facet.value} ({facet.count})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">Emotional Tone</label>
                  <select
                    value={filters.emotional_tone}
                    onChange={(e) => updateFilter('emotional_tone', e.target.value)}
                    className="w-full px-3 py-2 border rounded-md"
                  >
                    <option value="">All Tones</option>
                    {searchResults.facets.emotional_tones.map((facet) => (
                      <option key={facet.value} value={facet.value}>
                        {facet.value} ({facet.count})
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {getActiveFiltersCount() > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {Object.entries(filters).map(
                    ([key, value]) =>
                      value && (
                        <span
                          key={key}
                          className="inline-flex items-center gap-1 px-3 py-1 bg-primary/10 text-primary rounded-full text-sm"
                        >
                          {key}: {value}
                          <button
                            onClick={() => clearFilter(key)}
                            className="hover:bg-primary/20 rounded-full p-0.5"
                          >
                            <X className="h-3 w-3" />
                          </button>
                        </span>
                      )
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {loading && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Searching...</p>
          </div>
        )}

        {!loading && searchResults && (
          <div>
            <div className="mb-4">
              <p className="text-muted-foreground">
                Found {searchResults.total} results for &quot;{searchResults.query}&quot;
              </p>
            </div>

            {searchResults.results.length === 0 ? (
              <Card>
                <CardContent className="py-12 text-center">
                  <p className="text-muted-foreground">No memories found</p>
                </CardContent>
              </Card>
            ) : (
              <div className="space-y-4">
                {searchResults.results.map((result) => (
                  <Link key={result.id} href={`/dashboard/memories/${result.id}`}>
                    <Card className="hover:bg-accent transition-colors cursor-pointer">
                      <CardHeader>
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1">
                            <CardTitle className="text-xl">{result.title}</CardTitle>
                            {result.summary && (
                              <CardDescription className="mt-2">
                                {result.summary}
                              </CardDescription>
                            )}
                          </div>
                          {result.category && (
                            <span className="px-3 py-1 text-xs rounded-full bg-primary/10 text-primary whitespace-nowrap">
                              {result.category}
                            </span>
                          )}
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                          {result.date_of_event && (
                            <span className="flex items-center gap-1">
                              <Calendar className="h-4 w-4" />
                              {new Date(result.date_of_event).toLocaleDateString()}
                            </span>
                          )}
                          {result.location && (
                            <span className="flex items-center gap-1">
                              <MapPin className="h-4 w-4" />
                              {result.location}
                            </span>
                          )}
                          {result.emotional_tone && (
                            <span className={`flex items-center gap-1 px-2 py-1 rounded-full ${getEmotionColor(result.emotional_tone)}`}>
                              <Heart className="h-4 w-4" />
                              {result.emotional_tone}
                            </span>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
