### Process

My first impresion was to review the data, means the PDFs. I realized that the mayority of the pdf pages was images (ikea manuals). So after this I decided to use a multimodal approach instead of a OCR model that could interpretare letters in the images. 

Second I decided to do a preprocess of take the pdf and transform all to images. Then we will take this images and extract information and vectorize using a multimodal model as GPT-4o. 

For the metadata I just take the assumption that the pdf name will have the basic metadata of what is the manual about, but a point for improvision would be to create a ingestion pipeline with some extractors as TitleExtractor and also some custom extractors to summarize and information from the manuals, in order to add this as metadata. The metadata I take was only the one that was on the filename and path. 

For future also we could instead of have a simple folder with files, we could use a bucket as amazon s3 or aure storages.

Then I create a retriever to get the images from the query, using the metadata with some filters as the "item" or the image path itself. This retriever will deliver me all the images that are related with the query, using a multimodal model as we mentioned. Then we will deliver a answer from the model with the complete function and we will wrap this in an agent tool. A main react agent then will have a tool for retrieve this answer from images but also another tool for inject the proper values of the filters.

For the metrics we did a simple approach, doing manually a check of what images should the retriever give based on some questions, and then give to the multimodal to get an answer. Then I compare this answers with the ones of my multimodal. The only BUT here is that for this I didnt test the react agent, instead I test the custom retriever using a simple filter  choosing that would act as an "agent" to get the proper filter keyword to inject to the retriever (this also because the lack of time I have for this task)

We have some points that we could discuss to improve on this solution. First is that maybe I could ose more text vectors and not only images. Second is the improvement on the filters, fue my lack of time I just implemented a simple filtering, but could be better in order to add more metadata and improve the retrieval method. Also another improvement would be to do the metrics over the agent and check also some "hit" evaluation over the images nodes that I get and the images nodes that should be.

Extra:  
   I refactor and modularize the code into a Fast API and create some end-end solution for the ingestation process, and the quering, and is ready to be connected to some external clients as wrbplatforms, etc (no security layer added). 

   I attach a Dockerfile but is not done, because the agent cannot access to the files from the images folder, I will leave it incomplete to you review if you need it, but If I will have some time I would complete of course.