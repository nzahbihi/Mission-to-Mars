# Mission-to-Mars

## Analysis Overview
The purpose of this repository is to present information about Mars at a glance. To do this, we scraped data specifically from:
* https://redplanetscience.com
* https://spaceimages-mars.com
* https://galaxyfacts-mars.com
* https://marshemispheres.com/

The data extracted included latest news about the Mars Missions, images, and facts. The data was then stored in MongoDB, and presented in a readable format using Flask and Bootstrap.

## Resources
Software: Jupyter Notebook 6.4.8, Visual Studio Code 1.70.2, MongoDB 6.0 Community Edition.

## Results

![Screenshot 2022-08-19 at 17-09-09 Mission to Mars](https://user-images.githubusercontent.com/106129195/185721424-ff45d372-4cd9-47a1-b31b-f1e6ba6536ee.png)

We have built a readable display of various information about Mars. We have also included a button that, upon utilizing, will re-scrape the data and fetch any new information, e.g. the latest news story and featured image.
