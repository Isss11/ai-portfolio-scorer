# PyroMetric: ai-portfolio-scorer

<div align="center">
  <img width="400" src="backend/images/PyroMetricLogo.png" alt="PyroMetric Logo" />
</div>

# Overview

## Inspiration

As students who seem to never stop searching for jobs, we wanted to create a platform that would improve the landscape for employers when selecting candidates for an interview. It is often tough to determine how impressive a project is simply from its description. A good project could be held back by a bad description, and a poor project can be embellished with good writing. We wanted to create a platform that can score candidates' GitHub profiles. This allows employers to have a better sense of how qualified a candidate truly is, and can be used for feedback to take your GitHub profile to the next level.

## Solution

We built a platform that allows employers and job seekers alike a way to view the "strength" of their GitHub portfolio. As a job seeker, you can enter any GitHub profile and get a quick overview of a few key metrics such as global impact, overall experience and code quality. These same metrics are used in the employer view when comparing a list of select candidates. Based on the overall performance of a portfolio, the candidates get ranked from best to worst.

## Technologies

- Google Gemini
- GitHub Rest API
- GitHub GraphQL API
- React
- Vite
- Tailwind CSS
- Vercel
- Flask 
- Google Cloud Run
- Custom LLM model trained with Google Vertex AI
- TensorFlow
- Google Cloud Storage Bucket
- pnpm

## To Run

After installing all the dependencies cited above (many can be installed by simply running `pip install -r requirements.txt`), the application can be run by:

### Back-end

> `cd backend`

> `python main.py`

### Front-end

> `cd frontend`

> `pnpm dev`
