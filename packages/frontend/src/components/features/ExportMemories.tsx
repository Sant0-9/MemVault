'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import api from '@/lib/api'
import { Download, FileJson, FileText, FileSpreadsheet, Music } from 'lucide-react'

interface ExportMemoriesProps {
  elderId: number
  elderName: string
}

export default function ExportMemories({ elderId, elderName }: ExportMemoriesProps) {
  const [exporting, setExporting] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleExport = async (format: 'json' | 'csv' | 'markdown') => {
    setExporting(format)
    setError(null)

    try {
      const response = await api.get(
        `/export/elders/${elderId}/export/${format}`,
        {
          responseType: 'blob',
        }
      )

      const blob = new Blob([response.data], {
        type: response.headers['content-type'] || 'application/octet-stream',
      })

      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url

      const contentDisposition = response.headers['content-disposition']
      let filename = `memories_${elderName.replace(/\s+/g, '_')}.${format}`

      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }

      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (err: any) {
      setError(err.response?.data?.detail || `Failed to export as ${format.toUpperCase()}`)
    } finally {
      setExporting(null)
    }
  }

  const handleAudioCompilation = async () => {
    setExporting('audio')
    setError(null)

    try {
      const response = await api.get(`/export/elders/${elderId}/export/audio-compilation`)

      if (response.data.total_audio_files === 0) {
        setError('No audio files available for this elder')
        return
      }

      const downloadAll = confirm(
        `Download ${response.data.total_audio_files} audio files? This will open multiple download windows.`
      )

      if (downloadAll) {
        response.data.audio_files.forEach((file: any, index: number) => {
          setTimeout(() => {
            const link = document.createElement('a')
            link.href = file.url
            link.setAttribute('download', file.title || `memory_${file.id}.mp3`)
            document.body.appendChild(link)
            link.click()
            link.remove()
          }, index * 500)
        })
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to get audio compilation')
    } finally {
      setExporting(null)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Download className="h-5 w-5" />
          Export Memories
        </CardTitle>
        <CardDescription>
          Download memories in various formats for backup or sharing
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <Button
            variant="outline"
            className="justify-start"
            onClick={() => handleExport('json')}
            disabled={exporting !== null}
          >
            <FileJson className="h-4 w-4 mr-2" />
            {exporting === 'json' ? 'Exporting...' : 'Export as JSON'}
          </Button>

          <Button
            variant="outline"
            className="justify-start"
            onClick={() => handleExport('csv')}
            disabled={exporting !== null}
          >
            <FileSpreadsheet className="h-4 w-4 mr-2" />
            {exporting === 'csv' ? 'Exporting...' : 'Export as CSV'}
          </Button>

          <Button
            variant="outline"
            className="justify-start"
            onClick={() => handleExport('markdown')}
            disabled={exporting !== null}
          >
            <FileText className="h-4 w-4 mr-2" />
            {exporting === 'markdown' ? 'Exporting...' : 'Export as Markdown'}
          </Button>

          <Button
            variant="outline"
            className="justify-start"
            onClick={handleAudioCompilation}
            disabled={exporting !== null}
          >
            <Music className="h-4 w-4 mr-2" />
            {exporting === 'audio' ? 'Preparing...' : 'Download All Audio'}
          </Button>
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="bg-muted p-3 rounded-lg space-y-2 text-sm">
          <p className="font-medium">Export Formats:</p>
          <ul className="space-y-1 text-muted-foreground">
            <li><strong>JSON:</strong> Complete data export with all metadata</li>
            <li><strong>CSV:</strong> Spreadsheet-compatible format for analysis</li>
            <li><strong>Markdown:</strong> Human-readable document with full stories</li>
            <li><strong>Audio:</strong> Download all audio recordings individually</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  )
}
