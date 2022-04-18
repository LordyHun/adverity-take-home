# adverity-take-home
Take-home task for Adverity

## My initial thoughts
The task can be broken down to the following main sections:
- getting the data from SWAPI
- storing the metadata in the database
- storing the actual data in the filesystem
- visualizing this data to allow interaction for the user

### My solution
I've decided to containerize the whole solution for ease of installation.
You can build the container for the backend with the `docker compose build` command, and afterwards run it
with the `docker compose run -d` command.
The database needs to be prepared before first use, via the `docker compose run --rm django python manage.py migrate`
command.

#### Models
Since there are only Star Wars data collections in the system, there is only one model in, `SWDataCollection`, which
stores the basic metadata of the snapshots taken from SWAPI.

#### Data retrieval and storage
Since it was recommended, I've used `requests` to gather the data, page by page from the homeworld and characters
in the API endpoints. The functions used for this can be found in the `sw_collections/integrations` package.
- A lookup dictionary is created for matching the URL of the "homeworld" property of the characters, and stored in-memory
- Then the data for the characters is fetched from the API
- Data transformations are done in one step on the complete dataset
- And lastly, the data is saved in a CSV file

##### How to improve
If the dataset for the homeworlds would be larger, I would have used a more sophisticated method of storing it, for example,
a temporary PETL table (or a pandas DF, etc.).
Also, would the dataset for the characters be of a significant size, I would definitely run the transformation in batches
instead of doing it in one step.
(But let's be honest, I would probably offload the whole workload to Celery workers or something similar, you rarely
want to process a large dataset synchronously)

#### Reading the data
When required, the dataset contained in a snapshot is just fetched from the disk and passed to the `collection_detailed`
template for display. The view feeding the template has a parameter to customize how many rows need to be displayed.
 
#### Counters
Engineering work is always a compromise between multiple factors, and, due to the limited amount of time which I can
invest in a take-home exercise, I have decided to move the "counters" feature out of scope.
(the feature does not seem to be overly complicated, but requires adding at least new view, a Form, and using PETL
to filter the currently-opened dataset, which takes time to implement)

#### Tests
I have prepared a few unit tests to test basic data retrieval and storage.
Tests can be executed via the `docker compose run --rm django pytest`
The tests only cover a basic test of the "happy-path" for data retrieval and storage, and I have decided against
extending them to cover the API testing or edge cases.
##### How to improve
- cover the API too
- mock the SWAPI response to cover edge cases, error cases
