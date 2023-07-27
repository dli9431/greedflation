import React from "react";
import type { LoaderFunctionArgs } from "react-router-dom";
import {
    isRouteErrorResponse,
    json,
    Link,
    Outlet,
    useLoaderData,
    useRouteError,
    LoaderFunction
} from "react-router-dom";
import List from "./list";

export function Fallback() {
    return <p>Performing initial data "load"</p>;
}

export function Layout() {
    return (
        <>
            <List />
            <Outlet />
        </>
    );
}

export function RootErrorBoundary() {
    console.log('test')
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

export function projectLoader({ params }: LoaderFunctionArgs) {
    if (params.projectId === "unauthorized") {
        throw json({ contactEmail: "administrator@fake.com" }, { status: 401 });
    }

    if (params.projectId === "broken") {
        // Uh oh - in this flow we somehow didn't get our data nested under `project`
        // and instead got it at the root - this will cause a render error!
        return json({
            id: params.projectId,
            name: "Break Some Stuff",
            owner: "The Joker",
            deadline: "June 2022",
            cost: "FREE",
        });
    }

    return json({
        project: {
            id: params.projectId,
            name: "Build Some Stuff",
            owner: "Joe",
            deadline: "June 2022",
            cost: "$5,000 USD",
        },
    });
}

export function ProjectErrorBoundary() {
    let error = useRouteError();

    // We only care to handle 401's at this level, so if this is not a 401
    // ErrorResponse, re-throw to let the RootErrorBoundary handle it
    if (!isRouteErrorResponse(error) || error.status !== 401) {
        throw error;
    }

    return (
        <>
            <h1>You do not have access to this project</h1>
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