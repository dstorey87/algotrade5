import { useEffect } from 'react'
import { useDispatch } from 'react-redux'
import { AppDispatch } from '@/lib/store'
import { fetchTradeData } from '@/lib/slices/tradingSlice'

export function useDataPolling(interval: number = 5000) {
  const dispatch = useDispatch<AppDispatch>()

  useEffect(() => {
    // Initial fetch
    dispatch(fetchTradeData())

    // Set up polling interval
    const timer = setInterval(() => {
      dispatch(fetchTradeData())
    }, interval)

    // Cleanup on unmount
    return () => clearInterval(timer)
  }, [dispatch, interval])
}