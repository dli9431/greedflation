import React, { useState, useEffect } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { TextField, FormControl, InputLabel, Select, MenuItem, SelectChangeEvent, Checkbox, FormControlLabel } from '@mui/material';
import { Product } from './types/types';

export default function App() {
  const [data, setData] = useState<Product[]>([]);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const [showOnlyScraped, setShowOnlyScraped] = useState<boolean>(false);

  useEffect(() => {
    fetch('http://localhost:5000/api/get_all')
      .then(response => response.json())
      .then(data => {
        const modifiedData = data.map((item: any) => {
          console.log(item.scraped_nutrition)
          const mostRecentPrice = item.prices.reduce((prev: any, current: any) => {
            const prevDate = new Date(prev.date).getTime();
            const currentDate = new Date(current.date).getTime();
            return prevDate > currentDate ? prev : current;
          });
          return {
            product_code: item.product_code,
            name: item.name,
            brand: item.brand,
            url: item.url,
            price: mostRecentPrice.price,
            scraped_nutrition: item.scraped_nutrition,
            price_per_carb: item.price_per_carb,
            price_per_protein: item.price_per_protein,
            price_per_fat: item.price_per_fat,
            price_per_calorie: item.price_per_calorie,
            total_protein: item.total_protein,
            total_carb: item.total_carb,
            total_fat: item.total_fat,
            total_calories: item.total_calories,
          };
        });
        setData(modifiedData);
      });
  }, []);

  const handleSortOrderChange = (event: SelectChangeEvent<"asc" | "desc">) => {
    setSortOrder(event.target.value as 'asc' | 'desc');
  };
  const handleShowOnlyScrapedChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setShowOnlyScraped(event.target.checked);
  };
  const filteredData = data.filter(item => {
    if (showOnlyScraped) {
      return item.name.toLowerCase().includes(searchTerm.toLowerCase()) && item.scraped_nutrition;
    } else {
      return item.name.toLowerCase().includes(searchTerm.toLowerCase());
    }
  });
  const sortedData = filteredData.sort((a, b) => sortOrder === 'asc' ? a.price - b.price : b.price - a.price);

  return (
    <div>
      <TextField
        label="Search by item name"
        value={searchTerm}
        onChange={(event) => setSearchTerm(event.target.value)}
      />
      <FormControl>
        <InputLabel>Sort by price</InputLabel>
        <Select value={sortOrder} onChange={handleSortOrderChange}>
          <MenuItem value="asc">Low to high</MenuItem>
          <MenuItem value="desc">High to low</MenuItem>
        </Select>
      </FormControl>
      <FormControlLabel
        control={<Checkbox checked={showOnlyScraped} onChange={handleShowOnlyScrapedChange} />}
        label="Show only scraped nutrition"
      />
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Brand</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>URL</TableCell>
              <TableCell>Product Code</TableCell>
              <TableCell>Price</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedData.map((item: Product) => (
              <TableRow key={item.product_code}>
                <TableCell>{item.brand}</TableCell>
                <TableCell>{item.name}</TableCell>
                <TableCell>{item.url}</TableCell>
                <TableCell>{item.product_code}</TableCell>
                <TableCell>{item.price}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  )
}