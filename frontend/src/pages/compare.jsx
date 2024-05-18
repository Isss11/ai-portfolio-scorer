import { Navbar } from "@/components/navbar";
import { PageContainer } from "@/components/page-container";

export function ComparePage() {
    return (
        <PageContainer>
            <Navbar />
            <textarea id="compareInput" name="compareInput" rows="4" cols="10"></textarea>
        </PageContainer>
    );
}
