import { useRef, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import StagePipeline from '../components/StagePipeline'
import LogEntry from '../components/LogEntry'
import { formatBytes, formatDuration } from '../utils/format'

export default function PipelinePage({
  stages,
  progress,
  validation,
  logs,
  metrics,
  streamingText,
  candidateContent,
  running,
  connected,
  onRunStage
}) {
  const logsEndRef = useRef(null)
  const streamingRef = useRef(null)

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  useEffect(() => {
    if (streamingRef.current) {
      streamingRef.current.scrollTop = streamingRef.current.scrollHeight
    }
  }, [streamingText])

  const totalInput = stages.fetch.input_size
  const totalOutput = stages.assemble.output_size
  const overallRatio = totalInput > 0 ? totalOutput / totalInput : 0

  return (
    <>
      <div className="grid grid-cols-4 gap-3 mb-6">
        <MetricCard label="Total Input" value={totalInput > 0 ? formatBytes(totalInput) : '-'} />
        <MetricCard label="Total Output" value={totalOutput > 0 ? formatBytes(totalOutput) : '-'} />
        <MetricCard
          label="Compression"
          value={overallRatio > 0 ? `${(overallRatio * 100).toFixed(2)}%` : '-'}
          highlight={overallRatio > 0 && overallRatio < 0.05}
        />
        <MetricCard
          label="Duration"
          value={metrics?.total_duration ? formatDuration(metrics.total_duration) : '-'}
        />
      </div>

      <StagePipeline
        stages={stages}
        progress={progress}
        validation={validation}
        onRun={onRunStage}
        disabled={running || !connected}
      />

      {stages.assemble.status === 'running' && streamingText && (
        <div className="mb-3 p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/50">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-medium text-zinc-400">LLM Output (streaming)</h3>
            <span className="text-xs text-zinc-500">{streamingText.length.toLocaleString()} chars</span>
          </div>
          <div
            ref={streamingRef}
            className="h-48 overflow-y-auto bg-zinc-950/50 rounded p-2 font-mono text-xs text-zinc-300 whitespace-pre-wrap"
          >
            {streamingText}
          </div>
        </div>
      )}

      <ValidationErrors validation={validation} />

      {candidateContent && stages.assemble.status !== 'running' && (
        <div className="mb-3 p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/50">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs font-medium text-zinc-400">Generated Documentation</h3>
            <span className="text-xs text-zinc-500">{candidateContent.length.toLocaleString()} chars</span>
          </div>
          <div className="h-96 rounded overflow-hidden border border-zinc-800/50">
            <Editor
              height="100%"
              defaultLanguage="markdown"
              value={candidateContent}
              theme="vs-dark"
              options={{
                readOnly: true,
                minimap: { enabled: false },
                fontSize: 12,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                wordWrap: 'on',
                padding: { top: 8, bottom: 8 }
              }}
            />
          </div>
        </div>
      )}

      <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/50">
        <h3 className="text-xs font-medium text-zinc-400 mb-2">Event Log</h3>
        <div className="h-40 overflow-y-auto bg-zinc-950/50 rounded p-2">
          {logs.length === 0 ? (
            <div className="text-zinc-600 text-xs">No events yet</div>
          ) : (
            logs.map((log, i) => <LogEntry key={i} event={log} />)
          )}
          <div ref={logsEndRef} />
        </div>
      </div>
    </>
  )
}

function ValidationErrors({ validation }) {
  const strict = validation?.strict_validation || validation?.strict_check
  const syntax = validation?.syntax_verification
  const errors = strict?.errors || []
  const syntaxIssues = syntax
    ? Object.entries(syntax).filter(([, v]) => v.found && !v.correct)
    : []

  if (errors.length === 0 && syntaxIssues.length === 0) return null

  return (
    <div className="mb-3 p-3 bg-zinc-900/60 rounded-lg border border-red-900/30">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-xs font-medium text-red-400">
          Validation Errors ({errors.length + syntaxIssues.length})
        </h3>
        {strict && (
          <span className="text-xs text-zinc-500">
            {strict.passed}/{strict.passed + strict.failed} blocks pass
            {strict.skipped > 0 && ` (${strict.skipped} skipped)`}
          </span>
        )}
      </div>
      <div className="max-h-64 overflow-y-auto space-y-1.5">
        {errors.map((err, i) => (
          <div key={`jac-${i}`} className="p-2 bg-zinc-950/60 rounded border border-zinc-800/50">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-medium text-red-400">jac check</span>
              <span className="text-xs text-zinc-500">[{err.source}:{err.line}]</span>
            </div>
            <div className="text-xs text-amber-300 font-mono">{err.error}</div>
            {err.code && (
              <div className="mt-1 text-xs text-zinc-500 font-mono truncate">{err.code}</div>
            )}
          </div>
        ))}
        {syntaxIssues.map(([name, info]) => (
          <div key={`syn-${name}`} className="p-2 bg-zinc-950/60 rounded border border-zinc-800/50">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-medium text-amber-400">syntax</span>
              <span className="text-xs text-zinc-500">{name}</span>
            </div>
            <div className="text-xs text-zinc-400">Expected: <span className="text-zinc-300 font-mono">{info.expected}</span></div>
          </div>
        ))}
      </div>
    </div>
  )
}

function MetricCard({ label, value, highlight }) {
  return (
    <div className="p-3 bg-zinc-900/60 rounded-lg border border-zinc-800/50">
      <div className="text-zinc-500 text-xs mb-1">{label}</div>
      <div className={`text-lg font-semibold ${highlight ? 'text-emerald-400' : ''}`}>{value}</div>
    </div>
  )
}
