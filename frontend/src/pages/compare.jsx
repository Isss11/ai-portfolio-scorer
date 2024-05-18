import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";
import { Button } from "@/components/ui/button";

export function ComparePage() {
    return (
        <PageContainer>
            <Navbar />
            <h1>Compare GitHub User Profiles</h1>
            <textarea id="compareInput" name="compareInput" rows="4" cols="10" placeholder="Enter a list of users' GitHub profile URLs, with each URL on a separate line."></textarea>
            <Button>Compare Profiles</Button>
        </PageContainer>
    );
}
