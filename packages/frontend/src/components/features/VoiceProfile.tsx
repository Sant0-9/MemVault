'use client'

import { useState, useCallback } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Loader2, Mic, Trash2, Play } from 'lucide-react'
import api from '@/lib/api'

interface VoiceProfileProps {
  elderId: number
  elderName: string
  voiceProfile?: {
    has_voice: boolean
    voice_id?: string
    voice_name?: string
    sample_audios?: any
  }
  onVoiceCreated?: () => void
}

export default function VoiceProfile({
  elderId,
  elderName,
  voiceProfile,
  onVoiceCreated,
}: VoiceProfileProps) {
  const [isUploading, setIsUploading] = useState(false)
  const [audioFiles, setAudioFiles] = useState<File[]>([])
  const [voiceName, setVoiceName] = useState(elderName)
  const [description, setDescription] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<string | null>(null)
  const [isDeleting, setIsDeleting] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files)
      setAudioFiles(files)
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (audioFiles.length === 0) {
      setError('Please select at least one audio file')
      return
    }

    if (audioFiles.length > 10) {
      setError('Maximum 10 audio files allowed')
      return
    }

    setIsUploading(true)
    setError(null)
    setSuccess(null)

    try {
      const formData = new FormData()
      formData.append('name', voiceName)
      if (description) {
        formData.append('description', description)
      }

      audioFiles.forEach((file) => {
        formData.append('audio_files', file)
      })

      const response = await api.post(
        `/voice/elders/${elderId}/voice/clone`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )

      if (response.data.success) {
        setSuccess('Voice cloned successfully!')
        setAudioFiles([])
        setDescription('')
        onVoiceCreated?.()
      } else {
        setError(
          response.data.message +
            (response.data.quality_issues
              ? '\n\nIssues: ' + response.data.quality_issues.join(', ')
              : '')
        )
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to clone voice')
    } finally {
      setIsUploading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this voice profile?')) {
      return
    }

    setIsDeleting(true)
    setError(null)

    try {
      await api.delete(`/voice/elders/${elderId}/voice`)
      setSuccess('Voice profile deleted successfully')
      onVoiceCreated?.()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete voice profile')
    } finally {
      setIsDeleting(false)
    }
  }

  if (voiceProfile?.has_voice) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2">
                <Mic className="h-5 w-5" />
                Voice Profile
              </CardTitle>
              <CardDescription>
                Voice clone is active for {voiceProfile.voice_name}
              </CardDescription>
            </div>
            <Button
              variant="destructive"
              size="sm"
              onClick={handleDelete}
              disabled={isDeleting}
            >
              {isDeleting ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  <Trash2 className="h-4 w-4 mr-2" />
                  Delete
                </>
              )}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <Label>Voice ID</Label>
              <p className="text-sm text-muted-foreground font-mono">
                {voiceProfile.voice_id}
              </p>
            </div>
            {success && (
              <Alert>
                <AlertDescription>{success}</AlertDescription>
              </Alert>
            )}
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Mic className="h-5 w-5" />
          Create Voice Clone
        </CardTitle>
        <CardDescription>
          Upload audio samples to create a voice clone for AI-generated memories
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="voice-name">Voice Name</Label>
          <Input
            id="voice-name"
            value={voiceName}
            onChange={(e) => setVoiceName(e.target.value)}
            placeholder="Enter voice name"
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="description">Description (Optional)</Label>
          <Textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe the voice characteristics..."
            rows={3}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="audio-files">Audio Samples</Label>
          <Input
            id="audio-files"
            type="file"
            accept="audio/*"
            multiple
            onChange={handleFileChange}
          />
          <p className="text-xs text-muted-foreground">
            Upload 3-5 clear audio samples (1-5 minutes total). Supported formats: MP3,
            WAV, M4A, OGG, FLAC
          </p>
          {audioFiles.length > 0 && (
            <div className="mt-2">
              <p className="text-sm font-medium">Selected files:</p>
              <ul className="text-sm text-muted-foreground list-disc list-inside">
                {audioFiles.map((file, index) => (
                  <li key={index}>{file.name}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {error && (
          <Alert variant="destructive">
            <AlertDescription className="whitespace-pre-line">{error}</AlertDescription>
          </Alert>
        )}

        {success && (
          <Alert>
            <AlertDescription>{success}</AlertDescription>
          </Alert>
        )}

        <div className="bg-muted p-4 rounded-lg space-y-2">
          <p className="text-sm font-medium">Tips for best results:</p>
          <ul className="text-sm text-muted-foreground space-y-1 list-disc list-inside">
            <li>Use clear, high-quality recordings</li>
            <li>Avoid background noise</li>
            <li>Include varied emotional expressions</li>
            <li>Ensure consistent recording quality</li>
            <li>Aim for 1-5 minutes total duration</li>
          </ul>
        </div>

        <Button
          onClick={handleUpload}
          disabled={isUploading || audioFiles.length === 0}
          className="w-full"
        >
          {isUploading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Cloning Voice...
            </>
          ) : (
            <>
              <Mic className="mr-2 h-4 w-4" />
              Clone Voice
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  )
}
