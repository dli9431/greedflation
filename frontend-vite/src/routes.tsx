import type { LoaderFunctionArgs } from "react-router-dom";
import {
    isRouteErrorResponse,
    json,
    Link,
    Outlet,
    useLoaderData,
    useRouteError,
    LoaderFunction,
    useMatch
} from "react-router-dom";
import List from "./list";
import { Product } from './types/types';
import ResponsiveNavMenu from "./nav";

export function Fallback() {
    return <p>Performing initial data "load"</p>;
}

export function Layout() {
    const isIndexPage = useMatch('/');

    return (
        <>
            <ResponsiveNavMenu />
            {isIndexPage && <List />}
            <Outlet />    
        </>
    );
}

export function RootErrorBoundary() {
    let error = useRouteError() as Error;
    return (
        <div>
            <h1>Uh oh, something went terribly wrong 😩</h1>
            <pre>{error.message || JSON.stringify(error)}</pre>
            <button onClick={() => (window.location.href = "/")}>
                Click here to reload the app
            </button>
        </div>
    );
}
export async function productLoader({ params }: LoaderFunctionArgs) {
    console.log('test')
    console.log(params)
    const product: Product = await fetch(`http://localhost:5000/api/product?product_code=${params.productid}&store=`).then((res) => res.json());
    console.log(product);
    return json(product);
    // if (params.productId === "unauthorized") {
    //     throw json({ contactEmail: "administrator@fake.com" }, { status: 401 });
    // }

    // if (params.productId === "broken") {
    //     // Uh oh - in this flow we somehow didn't get our data nested under `project`
    //     // and instead got it at the root - this will cause a render error!
    //     return json({
    //         id: params.projectId,
    //         name: "Break Some Stuff",
    //         owner: "The Joker",
    //         deadline: "June 2022",
    //         cost: "FREE",
    //     });
    // }

    // return json({
    //     product: {
    //         id: params.productId,
    //         name: params.name,
    //         product_code: params.product_code,
    //     },
    // });
}

export function ProductView() {
    const product = useLoaderData() as Product;

    return (
        <>
            <h1>Product: {product.name}</h1>
            <p>Product Code: {product.product_code}</p>
            <p>Brand: {product.brand}</p>
            <p>URL: {product.url}</p>
            <p>Price: {product.price}</p>
            <p>Scraped Nutrition: {product.scraped_nutrition}</p>
            <p>Price per Protein: {product.price_per_protein}</p>
            <p>Total Protein: {product.total_protein}</p>
            <p>Total Carb: {product.total_carb}</p>
            <p>Price per Carb: {product.price_per_carb}</p>
            <p>Total Fat: {product.total_fat}</p>
            <p>Price per Fat: {product.price_per_fat}</p>
            <p>Total Calories: {product.total_calories}</p>
            <p>Price per Calories: {product.price_per_calories}</p>
            <p>Total Fiber: {product.total_fiber}</p>
            <p>Price per Fiber: {product.price_per_fiber}</p>
            {/* <p>Owner: {data.owner}</p>
          <p>Deadline: {Project.deadline}</p>
          <p>Cost: {Project.cost}</p> */}
        </>
    );
}

export function ProductErrorBoundary() {
    let error = useRouteError();

    // We only care to handle 401's at this level, so if this is not a 401
    // ErrorResponse, re-throw to let the RootErrorBoundary handle it
    if (!isRouteErrorResponse(error) || error.status !== 401) {
        throw error;
    }

    return (
        <>
            <h1>You do not have access to this product</h1>
            <p>
                Please reach out to{" "}
                <a href={`mailto:${error.data.contactEmail}`}>
                    {error.data.contactEmail}
                </a>{" "}
                to obtain access.
            </p>
        </>
    );
}