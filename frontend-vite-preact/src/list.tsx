import { h, Fragment } from 'preact';
import { useState, useEffect } from 'preact/hooks';
import { TextField, FormControl, InputLabel, Select, MenuItem, Checkbox, FormControlLabel, TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Paper } from '@mui/material';
import { Product } from './types/types';

export default function List() {
    const [modifiedData, setData] = useState<Product[]>([]);
    const [searchTerm, setSearchTerm] = useState<string>('');
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
    const [showOnlyScraped, setShowOnlyScraped] = useState<boolean>(false);
    const [sortColumn, setSortColumn] = useState<keyof Product>('name');

    useEffect(() => {
        fetch('http://localhost:5000/api/get_all')
            .then(response => response.json())
            .then(data => {
                const modifiedData = data.map((item: any) => {
                    const mostRecentPrice = item.prices.reduce((prev: any, current: any) => {
                        const prevDate = new Date(prev.date).getTime();
                        const currentDate = new Date(current.date).getTime();
                        return prevDate > currentDate ? prev : current;
                    });
                    return {
                        product_code: item.product_code,
                        name: item.brand ? `${item.brand} ${item.name}` : item.name,
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

    const handleSort = (column: keyof Product) => {
        if (column === sortColumn) {
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
            setSortColumn(column);
            setSortOrder('asc');
        }
    };
    const handleSortOrderChange = (event: any) => {
        setSortOrder(event.target.value);
    };
    const handleShowOnlyScrapedChange = (event: any) => {
        setShowOnlyScraped(event.target.checked);
    };
    const handleSearchTermChange = (event: any) => {
        setSearchTerm(event.target.value);
    };
    const filteredData = modifiedData.filter(item => {
        if (showOnlyScraped) {
            return item.name.toLowerCase().includes(searchTerm.toLowerCase()) && item.scraped_nutrition;
        } else {
            return item.name.toLowerCase().includes(searchTerm.toLowerCase());
        }
    });
    const sortedData = modifiedData
        .filter((item: Product) => showOnlyScraped ? item.is_scraped : true)
        .filter((item: Product) => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
        .sort((a: Product, b: Product) => {
            const sortValue = sortOrder === 'asc' ? 1 : -1;
            if (!a[sortColumn]) {
                return sortValue;
            }
            if (!b[sortColumn]) {
                return -sortValue;
            }
            if (a[sortColumn] < b[sortColumn]) {
                return -sortValue;
            }
            if (a[sortColumn] > b[sortColumn]) {
                return sortValue;
            }
            return 0;
        });

    return (
        <Fragment>
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
                <Table border={1}>
                    <TableHead>
                        <TableRow>
                            <TableCell onClick={() => handleSort('name')}>Name</TableCell>
                            <TableCell onClick={() => handleSort('price')}>Price</TableCell>
                            <TableCell onClick={() => handleSort('total_protein')}>Total Protein</TableCell>
                            <TableCell onClick={() => handleSort('price_per_protein')}>Price per protein</TableCell>
                            <TableCell onClick={() => handleSort('product_code')}>Product Code</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {sortedData.map((item: Product) => (
                            <TableRow key={item.product_code}>
                                <TableCell style={{ width: '25%', padding: 2 }}>
                                    {item.name}
                                </TableCell>
                                <TableCell style={{ padding: 2 }}>{item.price}</TableCell>
                                <TableCell style={{ padding: 2 }}>{item.total_protein}</TableCell>
                                <TableCell style={{ padding: 2 }}>{item.price_per_protein}</TableCell>
                                <TableCell style={{ padding: 2 }}>{item.product_code}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Fragment>
    );
}
// import { useState, useEffect } from 'preact/hooks';
// import { TextField, FormControl, InputLabel, Select, MenuItem, Checkbox, FormControlLabel, TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Paper } from '@mui/material';
// import { Product } from './types/types';

// export default function List() {
//     const [modifiedData, setData] = useState<Product[]>([]);
//     const [searchTerm, setSearchTerm] = useState<string>('');
//     const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
//     const [showOnlyScraped, setShowOnlyScraped] = useState<boolean>(false);
//     const [sortColumn, setSortColumn] = useState<keyof Product>('name');

//     useEffect(() => {
//         fetch('http://localhost:5000/api/get_all')
//             .then(response => response.json())
//             .then(data => {
//                 const modifiedData = data.map((item: any) => {
//                     const mostRecentPrice = item.prices.reduce((prev: any, current: any) => {
//                         const prevDate = new Date(prev.date).getTime();
//                         const currentDate = new Date(current.date).getTime();
//                         return prevDate > currentDate ? prev : current;
//                     });
//                     return {
//                         product_code: item.product_code,
//                         name: item.brand ? `${item.brand} ${item.name}` : item.name,
//                         url: item.url,
//                         price: mostRecentPrice.price,
//                         scraped_nutrition: item.scraped_nutrition,
//                         price_per_carb: item.price_per_carb,
//                         price_per_protein: item.price_per_protein,
//                         price_per_fat: item.price_per_fat,
//                         price_per_calorie: item.price_per_calorie,
//                         total_protein: item.total_protein,
//                         total_carb: item.total_carb,
//                         total_fat: item.total_fat,
//                         total_calories: item.total_calories,
//                     };
//                 });
//                 setData(modifiedData);
//             });
//     }, []);

//     const handleSort = (column: keyof Product) => {
//         if (column === sortColumn) {
//             setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
//         } else {
//             setSortColumn(column);
//             setSortOrder('asc');
//         }
//     };
//     const handleSortOrderChange = (event: any) => {
//         setSortOrder(event.target.value);
//     };
//     const handleShowOnlyScrapedChange = (event: any) => {
//         setShowOnlyScraped(event.target.checked);
//     };
//     const handleSearchTermChange = (event: any) => {
//         setSearchTerm(event.target.value);
//     };
//     const filteredData = modifiedData.filter(item => {
//         if (showOnlyScraped) {
//             return item.name.toLowerCase().includes(searchTerm.toLowerCase()) && item.scraped_nutrition;
//         } else {
//             return item.name.toLowerCase().includes(searchTerm.toLowerCase());
//         }
//     });
//     const sortedData = modifiedData
//         .filter((item: Product) => showOnlyScraped ? item.is_scraped : true)
//         .filter((item: Product) => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
//         .sort((a: Product, b: Product) => {
//             const sortValue = sortOrder === 'asc' ? 1 : -1;
//             if (!a[sortColumn]) {
//                 return sortValue;
//             }
//             if (!b[sortColumn]) {
//                 return -sortValue;
//             }
//             if (a[sortColumn] < b[sortColumn]) {
//                 return -sortValue;
//             }
//             if (a[sortColumn] > b[sortColumn]) {
//                 return sortValue;
//             }
//             return 0;
//         });

//     return (
//         <div>
//             <TextField
//                 label="Search by item name"
//                 value={searchTerm}
//                 onChange={(event) => setSearchTerm(event.target.value)}
//             />
//             <FormControl>
//                 <InputLabel>Sort by price</InputLabel>
//                 <Select value={sortOrder} onChange={handleSortOrderChange}>
//                     <MenuItem value="asc">Low to high</MenuItem>
//                     <MenuItem value="desc">High to low</MenuItem>
//                 </Select>
//             </FormControl>
//             <FormControlLabel
//                 control={<Checkbox checked={showOnlyScraped} onChange={handleShowOnlyScrapedChange} />}
//                 label="Show only scraped nutrition"
//             />
//             <TableContainer component={Paper}>
//                 <Table border={1}>
//                     <TableHead>
//                         <TableRow>
//                             <TableCell onClick={() => handleSort('name')}>Name</TableCell>
//                             <TableCell onClick={() => handleSort('price')}>Price</TableCell>
//                             <TableCell onClick={() => handleSort('total_protein')}>Total Protein</TableCell>
//                             <TableCell onClick={() => handleSort('price_per_protein')}>Price per protein</TableCell>
//                             <TableCell onClick={() => handleSort('product_code')}>Product Code</TableCell>
//                         </TableRow>
//                     </TableHead>
//                     <TableBody>
//                         {sortedData.map((item: Product) => (
//                             <TableRow key={item.product_code}>
//                                 <TableCell style={{ width: '25%', padding: 2 }}>
//                                     {item.name}
//                                 </TableCell>
//                                 <TableCell style={{ padding: 2 }}>{item.price}</TableCell>
//                                 <TableCell style={{ padding: 2 }}>{item.total_protein}</TableCell>
//                                 <TableCell style={{ padding: 2 }}>{item.price_per_protein}</TableCell>
//                                 <TableCell style={{ padding: 2 }}>{item.product_code}</TableCell>
//                             </TableRow>
//                         ))}
//                     </TableBody>
//                 </Table>
//             </TableContainer>
//         </div>
//     )
//     // return (
//     //     <div>
//     //         <TextField label="Search by item name" value={searchTerm} onChange={handleSearchTermChange} />
//     //         <FormControl>
//     //             <InputLabel>Sort by price</InputLabel>
//     //             <Select value={sortOrder} onChange={(event: SelectChangeEvent) => setSortOrder(event.target.value as 'asc' | 'desc')}>
//     //                 <MenuItem value="asc">Low to high</MenuItem>
//     //                 <MenuItem value="desc">High to low</MenuItem>
//     //             </Select>
//     //         </FormControl>
//     //         <FormControlLabel control={<Checkbox checked={showOnlyScraped} onChange={handleShowOnlyScrapedChange} />} label="Show only scraped items" />
//     //         <TableContainer component={Paper}>
//     //             <Table>
//     //                 <TableHead>
//     //                     <TableRow>
//     //                         <TableCell onClick={() => handleSort('name')}>Name</TableCell>
//     //                         <TableCell onClick={() => handleSort('price')}>Price</TableCell>
//     //                         <TableCell onClick={() => handleSort('total_protein')}>Total Protein</TableCell>
//     //                         <TableCell onClick={() => handleSort('price_per_protein')}>Price per protein</TableCell>
//     //                         <TableCell onClick={() => handleSort('product_code')}>Product Code</TableCell>
//     //                     </TableRow>
//     //                 </TableHead>
//     //                 <TableBody>
//     //                     {sortedData.map((item: Product) => (
//     //                         <TableRow key={item.product_code}>
//     //                             <TableCell style={{ width: '25%', padding: 2 }}>
//     //                                 <a href={`/products/${item.product_code}`}>{item.name}</a>
//     //                             </TableCell>
//     //                             <TableCell style={{ width: '25%', padding: 2 }}>{item.price}</TableCell>
//     //                             <TableCell style={{ width: '25%', padding: 2 }}>{item.total_protein}</TableCell>
//     //                             <TableCell style={{ width: '25%', padding: 2 }}>{item.price_per_protein}</TableCell>
//     //                             <TableCell style={{ width: '25%', padding: 2 }}>{item.product_code}</TableCell>
//     //                         </TableRow>
//     //                     ))}
//     //                 </TableBody>
//     //             </Table>
//     //         </TableContainer>
//     //     </div>
//     // );
// }