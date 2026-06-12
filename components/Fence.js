export default function Fence() {
  const posts = Array.from({ length: 22 }, (_, i) => i)
  const width = 100 / 21

  return (
    <svg
      className="fence"
      viewBox="0 0 1200 80"
      preserveAspectRatio="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ width: '100%', height: '60px' }}
    >
      {/* Two horizontal rails */}
      <rect x="0" y="22" width="1200" height="8"  rx="3" fill="#c8a97a"/>
      <rect x="0" y="50" width="1200" height="7"  rx="3" fill="#b8995a"/>

      {/* Vertical posts with pointed tops */}
      {posts.map(i => {
        const x = (i / 21) * 1160 + 20
        return (
          <g key={i}>
            <polygon
              points={`${x},2 ${x+12},2 ${x+16},18 ${x-4},18`}
              fill="#c8a97a"
            />
            <rect x={x} y="18" width="12" height="56" rx="2" fill="#b8995a"/>
            <rect x={x+2} y="18" width="3" height="56" rx="1" fill="rgba(255,255,255,0.15)"/>
          </g>
        )
      })}
    </svg>
  )
}
