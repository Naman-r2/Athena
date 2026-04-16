interface ErrorMessageProps {
  message?: string;
  onRetry?: () => void;
}

const ErrorMessage = ({ message = "Something went wrong.", onRetry }: ErrorMessageProps) => (
  <div className="flex flex-col items-center justify-center py-16 gap-3">
    <p className="text-sm text-destructive font-body">{message}</p>
    {onRetry && (
      <button
        onClick={onRetry}
        className="px-4 py-2 text-sm font-body font-medium bg-primary text-primary-foreground rounded-sm hover:opacity-90 transition-opacity"
      >
        Try Again
      </button>
    )}
  </div>
);

export default ErrorMessage;
