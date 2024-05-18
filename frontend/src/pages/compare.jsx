import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import axios from "axios"

export function ComparePage() {
    const [profiles, setProfiles] = useState("")

    const handleSubmit = async (e) => {
        // TODO: May change IP and port to something standardized
        let requestBody = {
            "profileLinks": profiles
        }

        let response = await axios.post("http://127.0.0.1:8080/compareProfiles", requestBody);

        // TODO: REMOVE later
        console.log({ response })
    }

    return (
        <PageContainer>
            <Navbar />
            <h1>Compare GitHub User Profiles</h1>
            <textarea id="compareInput" name="compareInput" rows="4" cols="10" value={profiles} onChange={(e) => setProfiles(e.target.value)} placeholder="Enter a list of users' GitHub profile URLs, with each URL on a separate line."></textarea>
            <Button onClick={(e) => handleSubmit(e)}>Compare Profiles</Button>
        </PageContainer>
    );
}
