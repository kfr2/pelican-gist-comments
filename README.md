# Pelican-Gist-Comments
Pelican-Gist-comments is a plugin for [Pelican](http://blog.getpelican.com/) that enables commenting on a site's articles via GitHub's Gists.

## REQUIREMENTS
 * [Requests](http://docs.python-requests.org/en/latest/)


## INSTALLATION
Download or clone this [repository](https://github.com/kfr2/pelican-gist-comments) to a `plugin` directory and rename it to something like `gist_comments`. Edit `pelicanconf.py` to include the following:

	GITHUB_USERNAME = 'kfr2'
	GITHUB_AUTH_TOKEN = '12345'
    PLUGIN_PATH = 'plugins/'
    PLUGINS = ('gist_comments', )

GitHub authentication tokens can be created on the [GitHub settings page](https://github.com/settings/applications) (under the "Personal API Access Token" section).

**Note:** I would **strongly** suggest you store the authentication token outside of version control. You may find success saving the token to a system environment variable and later retrieving it in your Pelican configuration file via `os.environ.get('VARIABLE_NAME')`.

See the [pelican plugins README](https://github.com/getpelican/pelican-plugins/) for more information.


## USAGE
As an article is processed into an HTML page, the plugin will examine `gist_comment_ids.json` to determine whether or not it contains a Gist ID for the article's slug. If it does not, a Gist will be created for the article via GitHub's API and its ID will be saved into the json file. The article will then have the metadata field `gist_id` added to it.

You may access the gist ID in a template via the following:

	{{ article.gist_id }}
	
For an example, please see [my pelican-foundation theme](https://github.com/kfr2/pelican-foundation/blob/master/templates/article.html#L19).


## AUTHORS
* [Kevin Richardson](https://github.com/kfr2)


## LICENSE
Released under the MIT License.  See full details in the `LICENSE` file.

