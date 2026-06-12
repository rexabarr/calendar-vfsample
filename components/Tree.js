import { useEffect, useRef } from 'react'

// stage: 0-7  (0=seed, 7=full bloom)
// dying: bool
// won: bool
export default function Tree({ stage, dying, won }) {
  const svgRef = useRef(null)

  // Trigger grow animation on each newly revealed layer
  useEffect(() => {
    if (!svgRef.current) return
    const layers = svgRef.current.querySelectorAll('.tree-layer')
    layers.forEach((el, i) => {
      if (i <= stage) {
        if (!el.classList.contains('visible')) {
          el.classList.add('visible')
        }
      } else {
        el.classList.remove('visible')
      }
    })
  }, [stage])

  const treeClass = [
    'tree-svg',
    dying ? 'tree-dying' : '',
    won   ? 'tree-won'   : '',
  ].join(' ')

  return (
    <svg
      ref={svgRef}
      className={treeClass}
      viewBox="0 0 320 440"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* ── GROUND SHADOW ── */}
      <ellipse cx="160" cy="435" rx="70" ry="8" fill="rgba(0,0,0,0.18)" />

      {/* ── LAYER 0: TRUNK + ROOTS (always visible) ── */}
      <g className="tree-layer tree-layer-0">
        {/* Roots */}
        <path className="branch" d="M148 400 Q138 415 125 420" stroke="#4a3020" strokeWidth="5" fill="none" strokeLinecap="round"/>
        <path className="branch" d="M160 405 Q158 420 152 428" stroke="#4a3020" strokeWidth="5" fill="none" strokeLinecap="round"/>
        <path className="branch" d="M172 400 Q182 415 195 420" stroke="#4a3020" strokeWidth="5" fill="none" strokeLinecap="round"/>
        {/* Main trunk */}
        <path
          className="trunk"
          d="M145 405 Q140 360 148 310 Q152 270 155 230 Q158 200 160 170"
          stroke="#5D4037" strokeWidth="22" fill="none" strokeLinecap="round"
        />
        <path
          className="trunk"
          d="M175 405 Q180 360 172 310 Q168 270 165 230 Q162 200 160 170"
          stroke="#6D4C41" strokeWidth="16" fill="none" strokeLinecap="round"
        />
        {/* Bark texture */}
        <path d="M155 370 Q158 355 156 340" stroke="#4a3020" strokeWidth="2" fill="none" opacity="0.5"/>
        <path d="M165 350 Q163 335 164 320" stroke="#4a3020" strokeWidth="2" fill="none" opacity="0.5"/>
        <path d="M158 300 Q161 285 159 270" stroke="#4a3020" strokeWidth="2" fill="none" opacity="0.5"/>
      </g>

      {/* ── LAYER 1: FIRST BRANCH PAIR + SMALL LEAVES ── */}
      <g className="tree-layer">
        <path className="branch" d="M160 340 Q135 320 115 310" stroke="#6D4C41" strokeWidth="11" fill="none" strokeLinecap="round"/>
        <path className="branch" d="M160 340 Q185 320 205 310" stroke="#6D4C41" strokeWidth="11" fill="none" strokeLinecap="round"/>
        {/* Small leaf clusters at branch tips */}
        <g className="leaf-group">
          {[
            [105, 302], [118, 295], [97, 295],
          ].map(([cx, cy], i) => (
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="14" ry="10" fill="#4a8f2a" transform={`rotate(${i*25-15} ${cx} ${cy})`}/>
          ))}
        </g>
        <g className="leaf-group">
          {[
            [215, 302], [202, 295], [223, 295],
          ].map(([cx, cy], i) => (
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="14" ry="10" fill="#5aa030" transform={`rotate(${i*25-15} ${cx} ${cy})`}/>
          ))}
        </g>
      </g>

      {/* ── LAYER 2: SECOND BRANCH PAIR ── */}
      <g className="tree-layer">
        <path className="branch" d="M160 295 Q130 272 108 260" stroke="#795548" strokeWidth="9" fill="none" strokeLinecap="round"/>
        <path className="branch" d="M160 295 Q190 272 212 260" stroke="#795548" strokeWidth="9" fill="none" strokeLinecap="round"/>
        <g className="leaf-group">
          {[[98,252],[112,244],[90,245],[116,256]].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="16" ry="11" fill="#55a030" transform={`rotate(${i*30-30} ${cx} ${cy})`}/>
          ))}
        </g>
        <g className="leaf-group">
          {[[222,252],[208,244],[230,245],[204,256]].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="16" ry="11" fill="#4a8f28" transform={`rotate(${i*30-30} ${cx} ${cy})`}/>
          ))}
        </g>
      </g>

      {/* ── LAYER 3: UPPER TRUNK SPLIT ── */}
      <g className="tree-layer">
        <path className="branch" d="M160 240 Q148 215 142 195" stroke="#8D6E63" strokeWidth="8" fill="none" strokeLinecap="round"/>
        <path className="branch" d="M160 240 Q172 215 178 195" stroke="#8D6E63" strokeWidth="8" fill="none" strokeLinecap="round"/>
        <g className="leaf-group">
          {[[138,185],[148,177],[128,180],[143,170]].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="17" ry="12" fill="#60b030" transform={`rotate(${i*22-22} ${cx} ${cy})`}/>
          ))}
        </g>
        <g className="leaf-group">
          {[[182,185],[172,177],[192,180],[177,170]].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="17" ry="12" fill="#55a030" transform={`rotate(${i*22-22} ${cx} ${cy})`}/>
          ))}
        </g>
      </g>

      {/* ── LAYER 4: WIDE MID-CANOPY ── */}
      <g className="tree-layer">
        <path className="branch" d="M155 210 Q118 195 95 185" stroke="#A1887F" strokeWidth="7" fill="none" strokeLinecap="round"/>
        <path className="branch" d="M165 210 Q202 195 225 185" stroke="#A1887F" strokeWidth="7" fill="none" strokeLinecap="round"/>
        <g className="leaf-group">
          {[[82,176],[96,168],[76,168],[102,176],[88,162]].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="18" ry="13" fill="#4ea828" transform={`rotate(${i*20-40} ${cx} ${cy})`}/>
          ))}
        </g>
        <g className="leaf-group">
          {[[238,176],[224,168],[244,168],[218,176],[232,162]].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="18" ry="13" fill="#5ab82e" transform={`rotate(${i*20-40} ${cx} ${cy})`}/>
          ))}
        </g>
      </g>

      {/* ── LAYER 5: CROWN BASE ── */}
      <g className="tree-layer">
        <path className="branch" d="M155 175 Q140 155 130 138" stroke="#BCAAA4" strokeWidth="6" fill="none" strokeLinecap="round"/>
        <path className="branch" d="M165 175 Q180 155 190 138" stroke="#BCAAA4" strokeWidth="6" fill="none" strokeLinecap="round"/>
        <g className="leaf-group">
          {[[118,128],[132,118],[108,121],[138,128],[122,112]].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="19" ry="14" fill="#56b030" transform={`rotate(${i*18-36} ${cx} ${cy})`}/>
          ))}
        </g>
        <g className="leaf-group">
          {[[202,128],[188,118],[212,121],[182,128],[198,112]].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="19" ry="14" fill="#4da826" transform={`rotate(${i*18-36} ${cx} ${cy})`}/>
          ))}
        </g>
        {/* Dense center foliage */}
        <g className="leaf-group">
          {[[152,155],[160,145],[168,155],[156,138],[164,138]].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="20" ry="15" fill="#3d9e1c" transform={`rotate(${i*15-30} ${cx} ${cy})`}/>
          ))}
        </g>
      </g>

      {/* ── LAYER 6: FULL CANOPY ── */}
      <g className="tree-layer">
        <path className="branch" d="M158 135 Q160 115 160 95" stroke="#BCAAA4" strokeWidth="5" fill="none" strokeLinecap="round"/>
        <path className="branch" d="M155 120 Q132 100 115 88" stroke="#BCAAA4" strokeWidth="5" fill="none" strokeLinecap="round"/>
        <path className="branch" d="M165 120 Q188 100 205 88" stroke="#BCAAA4" strokeWidth="5" fill="none" strokeLinecap="round"/>
        <g className="leaf-group">
          {[
            [102,78],[118,68],[92,70],[126,78],[110,62],
            [98,85],[116,56],
          ].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="20" ry="14" fill={i%2===0?'#4ea828':'#5ac030'} transform={`rotate(${i*16-48} ${cx} ${cy})`}/>
          ))}
        </g>
        <g className="leaf-group">
          {[
            [218,78],[202,68],[228,70],[194,78],[210,62],
            [222,85],[204,56],
          ].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="20" ry="14" fill={i%2===0?'#56b430':'#4aa820'} transform={`rotate(${i*16-48} ${cx} ${cy})`}/>
          ))}
        </g>
        <g className="leaf-group">
          {[
            [148,90],[162,80],[172,90],[156,70],[165,70],
            [145,78],[175,78],[158,60],
          ].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="22" ry="16" fill={i%3===0?'#3d9e1c':i%3===1?'#55b02c':'#67c040'} transform={`rotate(${i*12-36} ${cx} ${cy})`}/>
          ))}
        </g>
      </g>

      {/* ── LAYER 7: FULL BLOOM with flowers/fruits ── */}
      <g className="tree-layer">
        {/* Extra lush leaves at very top */}
        <g className="leaf-group">
          {[
            [155,48],[165,40],[148,38],[172,48],[160,30],
            [143,52],[177,52],[155,22],[165,22],
          ].map(([cx,cy],i)=>(
            <ellipse key={i} className="leaf" cx={cx} cy={cy} rx="18" ry="13" fill={i%2===0?'#2e8b1a':'#4aaf28'} transform={`rotate(${i*14-45} ${cx} ${cy})`}/>
          ))}
        </g>

        {/* Flowers scattered on canopy */}
        {[
          [108,65],[135,55],[160,42],[185,55],[213,65],
          [95,80],[230,80],[125,72],[196,72],
        ].map(([cx,cy],i)=>(
          <g key={i} className="leaf">
            {[0,60,120,180,240,300].map(angle=>{
              const rad = angle * Math.PI / 180
              return <ellipse key={angle} cx={cx + Math.cos(rad)*7} cy={cy + Math.sin(rad)*7} rx="5" ry="3" fill={i%3===0?'#ff9eb5':i%3===1?'#ffe082':'#ce93d8'} transform={`rotate(${angle} ${cx+Math.cos(rad)*7} ${cy+Math.sin(rad)*7})`}/>
            })}
            <circle cx={cx} cy={cy} r="4" fill="#fff176"/>
          </g>
        ))}

        {/* Fruits */}
        {[
          [100,100],[142,88],[178,88],[220,100],
          [122,108],[200,108],
        ].map(([cx,cy],i)=>(
          <g key={i} className="leaf">
            <circle cx={cx} cy={cy} r="7" fill={i%2===0?'#e53935':'#ff8f00'}/>
            <path d={`M${cx} ${cy-7} Q${cx+4} ${cy-13} ${cx+2} ${cy-16}`} stroke="#4a8f2a" strokeWidth="1.5" fill="none"/>
          </g>
        ))}
      </g>
    </svg>
  )
}
