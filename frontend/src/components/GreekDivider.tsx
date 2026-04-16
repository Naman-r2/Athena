const GreekDivider = ({ className = "" }: { className?: string }) => (
  <div className={`flex items-center justify-center gap-3 ${className}`}>
    <div className="h-px flex-1 max-w-16 bg-gradient-to-r from-transparent to-gold/40" />
    <svg width="24" height="12" viewBox="0 0 24 12" fill="none" className="text-gold/50">
      <path d="M12 0L14.5 4H9.5L12 0Z" fill="currentColor" />
      <path d="M12 12L9.5 8H14.5L12 12Z" fill="currentColor" />
      <rect x="0" y="5" width="6" height="2" rx="1" fill="currentColor" />
      <rect x="18" y="5" width="6" height="2" rx="1" fill="currentColor" />
    </svg>
    <div className="h-px flex-1 max-w-16 bg-gradient-to-l from-transparent to-gold/40" />
  </div>
);

export default GreekDivider;
