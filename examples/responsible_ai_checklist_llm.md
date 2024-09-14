# Responsible AI Checklist for LLM Projects

## 1. Project Motivation
- [ ] What is the problem you want to solve?
- [ ] Which strategic goal does this project align with?
- [ ] Why is an LLM approach more suitable than traditional ML methods?

## 2. Problem Definition
- [ ] What specific task(s) do you want the LLM to perform?
- [ ] What input data will you provide to the LLM?
- [ ] For each dataset, describe:
  - [ ] Volume (number of examples/documents)
  - [ ] Time range covered
  - [ ] Storage location and access method
  - [ ] Data generation process and update frequency
  - [ ] Potential biases or significant changes in the data
- [ ] What are the most relevant factors for the LLM to consider for your specific task?
- [ ] How many high-quality examples can you provide for few-shot learning or fine-tuning?
- [ ] If using data from human subjects, have they given informed consent with a clear understanding of the data uses?
- [ ] Have we considered and mitigated potential biases in data collection and survey design?
- [ ] Have we minimized exposure of personally identifiable information (PII) through anonymization or selective data collection?

## 3. Performance Measurement
- [ ] Do you have a baseline system or benchmark against which to compare?
  If yes:
  - [ ] How does it perform?
  - [ ] Do you have documentation on how it works? 
- [ ] How will you measure the accuracy of the LLM's outputs?
- [ ] How will you measure the effectiveness of the LLM's outputs?
- [ ] What is the minimum level of accuracy (performance metric) you expect?
- [ ] What would an ideal solution look like?
- [ ] Are there reference solutions (e.g. research papers)?
- [ ] Have we examined the data for possible sources of bias and taken steps to mitigate or address these biases?
- [ ] Are our visualizations, summary statistics, and reports designed to honestly represent the underlying data?

## 4. LLM-Specific Evaluation Metrics
- [ ] How well does the LLM's output align with the provided context (Faithfulness)?
- [ ] Are the generated responses pertinent to the given queries? (Answer relevancy)
- [ ] How effectively does the LLM retrieve relevant information from the context? (Context recall)
- [ ] How accurate is the information the LLM extracts from the context? (Context precision)
- [ ] How well does the LLM incorporate available context into its responses? (Context utilization)
- [ ] How accurately does the LLM identify and use named entities from the context? (Context entity recall)
- [ ] Have we tested model results for fairness with respect to different affected groups?
- [ ] Can we explain the decision the model made or cite source attribution in cases where a justification is needed?

## 5. Ethical Considerations
- [ ] How will you assess and mitigate potential biases in the LLM's outputs?
- [ ] What measures will you implement to prevent generating harmful or toxic content?
- [ ] How will you ensure the LLM respects privacy and data protection regulations?
- [ ] Have we ensured that the model does not rely on variables or proxies for variables that are unfairly discriminatory?
- [ ] Have we communicated the shortcomings, limitations, and biases of the model to relevant stakeholders in ways that can be generally understood?
- [ ] Have we taken steps to identify and prevent unintended uses and abuse of the model and do we have a plan to monitor these once the model is deployed?

## 6. Roadmap/Timeline
- [ ] Are there any deadlines to be aware of?
- [ ] When do you need to see the first results or a proof of concept?
- [ ] What is the target date for a production-ready solution?

## 7. Contacts/Stakeholders
- [ ] Who is the product manager/owner or technical business lead?
- [ ] Who can provide access to necessary datasets and resources?
- [ ] Who are the domain experts who understand the context and current processes?
- [ ] Who will be responsible for prompt engineering and fine-tuning?

## 8. Collaboration
- [ ] Establish regular update meetings between business and engineering teams
- [ ] Define critical participants and their roles
- [ ] Set up version control and issue tracking systems for prompts, fine-tuning scripts, and evaluation code.

## 9. User Research Aspects
- [ ] Have you developed user personas for your LLM-based solution?
- [ ] Is there a user journey map that incorporates LLM interactions?
- [ ] What research has been done on your domain's user expectations for LLM-powered systems?
- [ ] Have we sought to address blindspots in the analysis through engagement with relevant stakeholders?

## 10. End User (Targeted Customers) Definition
- [ ] Who are the primary end-users of the LLM-based solution?
- [ ] What are their primary goals when interacting with the system?
- [ ] What pain points do they experience with current solutions?
- [ ] What specific expectations do they have for an LLM-powered system?

## 11. End User Testing
- [ ] Can users successfully achieve their goals using the LLM-based solution?
- [ ] How does the LLM-driven solution compare to previous methods regarding user satisfaction and task completion?
- [ ] Is there a feedback mechanism for users to report issues or suggest improvements?
- [ ] How will you incorporate user feedback into prompt refinement or model fine-tuning?

## 12. Deployment and Monitoring
- [ ] How will you deploy the LLM-based solution (e.g., API, embedded model)?
- [ ] What monitoring systems will you implement to track performance and detect issues in production?
- [ ] How will you handle model updates and maintain consistency in outputs over time?
- [ ] Do we have a clear plan to monitor the model and its impacts after deployment?
- [ ] Have we discussed a plan for response if users are harmed by the results?
- [ ] Is there a way to turn off or roll back the model in production if necessary?

## 13. Continual Improvement
- [ ] How frequently will you review and update prompts or fine-tuning data?
- [ ] What process will you use to validate and roll out improvements to the production system?
- [ ] How will you stay informed about advancements in LLM technology and incorporate them into your project?
- [ ] Is the process of generating the analysis well documented and reproducible if we discover issues in the future?

