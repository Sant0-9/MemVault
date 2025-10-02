'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter, useParams } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import api from '@/lib/api'

interface Message {
  role: 'assistant' | 'user'
  content: string
  timestamp?: string
}

interface Elder {
  id: number
  name: string
}

export default function InterviewPage() {
  const router = useRouter()
  const params = useParams()
  const elderId = params.id as string
  const [elder, setElder] = useState<Elder | null>(null)
  const [sessionId, setSessionId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [initializing, setInitializing] = useState(true)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    initializeInterview()
  }, [elderId])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const initializeInterview = async () => {
    try {
      const elderResponse = await api.get(`/elders/${elderId}`)
      setElder(elderResponse.data)

      const sessionResponse = await api.post('/interviews/', {
        elder_id: parseInt(elderId),
        title: `Interview with ${elderResponse.data.name}`,
      })
      setSessionId(sessionResponse.data.id)

      const questionResponse = await api.post(
        `/interviews/${sessionResponse.data.id}/question`,
        {}
      )
      setMessages([
        {
          role: 'assistant',
          content: questionResponse.data.question,
        },
      ])
    } catch (error) {
      console.error('Failed to initialize interview:', error)
    } finally {
      setInitializing(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || !sessionId) return

    const userMessage: Message = {
      role: 'user',
      content: input.trim(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      await api.post(`/interviews/${sessionId}/response`, {
        response: input.trim(),
      })

      const questionResponse = await api.post(`/interviews/${sessionId}/question`, {})

      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: questionResponse.data.question,
        },
      ])
    } catch (error) {
      console.error('Failed to process message:', error)
    } finally {
      setLoading(false)
    }
  }

  if (initializing) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-muted-foreground">Initializing interview...</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              href="/dashboard"
              className="text-sm text-muted-foreground hover:text-foreground"
            >
              ← Back to Dashboard
            </Link>
            <div className="h-4 w-px bg-border" />
            <h1 className="text-xl font-semibold">
              Interview with {elder?.name}
            </h1>
          </div>
          <Button
            variant="outline"
            onClick={() => router.push(`/dashboard/elders/${elderId}`)}
          >
            End Interview
          </Button>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto">
        <div className="container mx-auto px-4 py-8 max-w-3xl">
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <Card
                  className={`max-w-[80%] p-4 ${
                    message.role === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                </Card>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <Card className="max-w-[80%] p-4 bg-muted">
                  <p className="text-sm text-muted-foreground">Thinking...</p>
                </Card>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>

      <div className="border-t bg-background">
        <div className="container mx-auto px-4 py-4 max-w-3xl">
          <form onSubmit={handleSubmit} className="flex gap-4">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your response..."
              disabled={loading}
              className="flex-1"
            />
            <Button type="submit" disabled={loading || !input.trim()}>
              Send
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
