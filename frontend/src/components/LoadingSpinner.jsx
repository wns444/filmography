export default function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center py-12">
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-4 border-netflix-light"></div>
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-netflix-accent animate-spin"></div>
      </div>
    </div>
  )
}
