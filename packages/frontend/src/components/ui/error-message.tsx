import { AlertCircle } from 'lucide-react'
import { Alert, AlertDescription, AlertTitle } from './alert'
import { Button } from './button'

interface ErrorMessageProps {
  title?: string
  message: string
  onRetry?: () => void
}

export function ErrorMessage({ title = 'Error', message, onRetry }: ErrorMessageProps) {
  return (
    <Alert variant="destructive">
      <AlertCircle className="h-4 w-4" />
      <AlertTitle>{title}</AlertTitle>
      <AlertDescription className="mt-2">
        {message}
        {onRetry && (
          <div className="mt-3">
            <Button variant="outline" size="sm" onClick={onRetry}>
              Try Again
            </Button>
          </div>
        )}
      </AlertDescription>
    </Alert>
  )
}
