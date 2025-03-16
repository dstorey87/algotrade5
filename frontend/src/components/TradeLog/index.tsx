import { useState } from 'react'
import {
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Box,
  TablePagination,
  Tooltip
} from '@mui/material'
import { styled } from '@mui/material/styles'
import { useSelector } from 'react-redux'
import { RootState } from '../../store'

const Item = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  color: theme.palette.text.secondary,
  height: '100%',
}))

interface Trade {
  id: number
  timestamp: string
  pair: string
  type: 'buy' | 'sell'
  entryPrice: number
  exitPrice: number
  amount: number
  profit: number
  profitPercentage: number
  strategy: string
  confidence: number
  patternValidated: boolean
  quantumValidated: boolean
  tags: string[]
}

const TradeLog = () => {
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(10)
  const { trades } = useSelector((state: RootState) => state.trading)

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage)
  }

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10))
    setPage(0)
  }

  return (
    <Item>
      <Typography variant="h6" gutterBottom>
        Trade Log
      </Typography>

      <TableContainer>
        <Table sx={{ minWidth: 650 }} size="small">
          <TableHead>
            <TableRow>
              <TableCell>Time</TableCell>
              <TableCell>Pair</TableCell>
              <TableCell>Type</TableCell>
              <TableCell align="right">Entry</TableCell>
              <TableCell align="right">Exit</TableCell>
              <TableCell align="right">Amount</TableCell>
              <TableCell align="right">P/L</TableCell>
              <TableCell>Strategy</TableCell>
              <TableCell align="right">Confidence</TableCell>
              <TableCell>Validation</TableCell>
              <TableCell>Tags</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {trades
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((trade: Trade) => (
                <TableRow key={trade.id} hover>
                  <TableCell>
                    {new Date(trade.timestamp).toLocaleTimeString()}
                  </TableCell>
                  <TableCell>{trade.pair}</TableCell>
                  <TableCell>
                    <Chip
                      label={trade.type}
                      color={trade.type === 'buy' ? 'success' : 'error'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="right">£{trade.entryPrice.toFixed(2)}</TableCell>
                  <TableCell align="right">
                    {trade.exitPrice ? `£${trade.exitPrice.toFixed(2)}` : '-'}
                  </TableCell>
                  <TableCell align="right">{trade.amount}</TableCell>
                  <TableCell
                    align="right"
                    sx={{
                      color: trade.profit >= 0 ? 'success.main' : 'error.main',
                      fontWeight: 'bold'
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
                      £{trade.profit.toFixed(2)}
                      <Typography variant="caption" sx={{ ml: 0.5 }}>
                        ({trade.profitPercentage.toFixed(2)}%)
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{trade.strategy}</TableCell>
                  <TableCell align="right">
                    <Tooltip title="AI Model Confidence">
                      <Chip
                        label={`${(trade.confidence * 100).toFixed(0)}%`}
                        color={
                          trade.confidence > 0.85 ? 'success' :
                          trade.confidence > 0.7 ? 'warning' : 'error'
                        }
                        size="small"
                      />
                    </Tooltip>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', gap: 0.5 }}>
                      <Tooltip title="Pattern Validation">
                        <Chip
                          label="P"
                          color={trade.patternValidated ? 'success' : 'error'}
                          size="small"
                        />
                      </Tooltip>
                      <Tooltip title="Quantum Validation">
                        <Chip
                          label="Q"
                          color={trade.quantumValidated ? 'success' : 'error'}
                          size="small"
                        />
                      </Tooltip>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                      {trade.tags.map((tag) => (
                        <Chip
                          key={tag}
                          label={tag}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </TableCell>
                </TableRow>
            ))}
            {trades.length === 0 && (
              <TableRow>
                <TableCell colSpan={11} align="center">
                  No trades found
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={trades.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Item>
  )
}

export default TradeLog
