'use client'

import { ChangeEvent, DragEvent, useCallback, useRef, useState } from 'react'
import styles from './analytics.module.css'
import { parseLoanCsv } from '@/lib/analyticsProcessor'
import type { LoanRow } from '@/types/analytics'

type Props = {
  onData: (rows: LoanRow[]) => void
}

type ValidationState =
  | { status: 'idle' }
  | { status: 'success'; message: string }
  | { status: 'error'; message: string }
  | { status: 'warning'; message: string }

export function LoanUploader({ onData }: Props) {
  const [isDragging, setIsDragging] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [validation, setValidation] = useState<ValidationState>({ status: 'idle' })
  const [fileName, setFileName] = useState<string>('')
  const inputRef = useRef<HTMLInputElement | null>(null)

  const processFile = useCallback(
    async (file: File) => {
      setIsProcessing(true)
      setValidation({ status: 'idle' })
      setFileName(file.name)

      try {
        const text = await file.text()
        const parsed = parseLoanCsv(text)

        const missingDpd = parsed.every((row) => !row.dpd_status)
        setValidation({
          status: missingDpd ? 'warning' : 'success',
          message:
            missingDpd
              ? `Loaded ${parsed.length} rows, but no DPD status was found. Roll-rate analytics may be limited.`
              : `Loaded ${parsed.length} rows successfully.`,
        })
        onData(parsed)
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Unable to parse CSV file'
        setValidation({ status: 'error', message })
      } finally {
        setIsProcessing(false)
      }
    },
    [onData],
  )

  const handleFileChange = useCallback(
    (event: ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0]
      if (!file) return
      void processFile(file)
    },
    [processFile],
  )

  const handleDrop = useCallback(
    (event: DragEvent<HTMLDivElement>) => {
      event.preventDefault()
      setIsDragging(false)
      const file = event.dataTransfer.files?.[0]
      if (file) {
        void processFile(file)
      }
    },
    [processFile],
  )

  const handleDragOver = useCallback((event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()

    const relatedTarget = event.relatedTarget as Node | null

    if (relatedTarget && event.currentTarget.contains(relatedTarget)) {
      return
    }

    setIsDragging(false)
  }, [])

  const resetState = useCallback(() => {
    setValidation({ status: 'idle' })
    setFileName('')
    if (inputRef.current) {
      inputRef.current.value = ''
    }
  }, [])

  return (
    <section className={styles.section}>
      <div className={styles.sectionHeader}>
        <p className={styles.sectionTitle}>Loan uploader</p>
        <p className={styles.sectionCopy}>
          Drag in loans.csv or copy the production extract; we handle currency symbols and quoted values.
        </p>
      </div>

      <div
        className={`${styles.uploadDropArea} ${isDragging ? styles.uploadHighlight : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          className={styles.uploadInputOverlay}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          disabled={isProcessing}
          aria-label="Upload loans.csv"
          ref={inputRef}
        />

        <p className={styles.sectionTitle} style={{ textTransform: 'none', letterSpacing: '0.04em' }}>
          {isProcessing ? 'Processing file…' : 'Drop your CSV here or browse'}
        </p>
        <p className={styles.sectionCopy}>We validate headers and skip empty rows automatically.</p>

        {fileName && (
          <div className={styles.fileBadge}>
            <span>{fileName}</span>
            <button type="button" onClick={resetState} className={styles.clearButton}>
              Clear
            </button>
          </div>
        )}
      </div>

      {validation.status !== 'idle' && (
        <div
          className={`${styles.validationMessage} ${
            validation.status === 'success'
              ? styles.statusSuccess
              : validation.status === 'warning'
              ? styles.statusWarning
              : styles.statusError
          }`}
        >
          <p className={styles.sectionCopy}>{validation.message}</p>
        </div>
      )}
    </section>
  )
}
