import click
import click_log
import logging
import words.words
import pathlib

app_name = "nameit"
context_settings = { 'auto_envvar_prefix' : 'NAMEIT' }
log = logging.getLogger(__name__)
click_log.basic_config(log)
def secho(*args, **kwargs):
    log = logging.getLogger(__name__)
    if log.level <= logging.INFO:
        return click.secho(*args, **kwargs)

@click.group(context_settings=context_settings)
@click.version_option()
@click_log.simple_verbosity_option(log)
def cli():
    '''
    A system to generate interesting names.

    Note, each command's options may be set as an environment variable. To do
    so, the name must start with NAMEIT, followed by the command, then the
    option. E.g.: to set the db-path option in init, set NAMEIT_INIT_DB_PATH.
    '''
    pass

@cli.command()
@click.argument("adjectives")
@click.argument("adverbs")
@click.argument("nouns")
@click.argument("verbs")
@click.option( "--db-path"
    , "-d"
    , default="{}/words.db".format(click.get_app_dir(app_name))
    , help="Set the location to write the words database. Note, you will also have to pass"
      + " --db-path to the name command in order to use this database.")
def init(adjectives, adverbs, nouns, verbs, db_path):
    """Initialize nameit words database.

    nameit uses an optimized database file to store the words it uses. This
    allows nameit to move more quickly, and keeps the number of visible files
    small. To set up this database, this command takes paths to ADJECTIVES,
    ADVERBS, NOUNS, and VERBS.

    Each argument is a path to a file of newline-delimited words, one per line.
    The tool will ingest the file, and use it to prepare the corresponding
    collection of words in the database. Invoking this tool clears any existing
    database, so use it with caution.
    """
    secho("Initialize database", fg="yellow", bold=True)
    log = logging.getLogger(__name__)
    db_path = pathlib.Path(db_path)
    db_dir = db_path.parent

    log.debug('(dirs (db "{}")) (paths (db "{}") (words (adjectives "{}") (adverbs "{}") (verbs "{}") (nouns "{}")))'.format
              (db_dir, db_path, adjectives, adverbs, nouns, verbs))

    log.info("Ensure {} exists to hold DB.".format(db_dir))
    db_dir.mkdir(parents=True, exist_ok=True)

    log.info("Initialize DB.")
    wdb = words.words.words(db_path)

    def check_path(path):
        if not pathlib.Path(path).exists():
            log.error("Path {} does not exist!".format(path))
            exit(1)

    check_path(adjectives)
    check_path(adverbs)
    check_path(nouns)
    check_path(verbs)

    wdb.initialize(pathlib.Path(adjectives), pathlib.Path(adverbs), pathlib.Path(nouns), pathlib.Path(verbs))

    log.info("done")
    pass

@cli.command()
@click.option("--number-of-names-wanted", "-n", default=1, help="Generate this many names. Names might be repeated.")
@click.option( "--db-path"
    , "-d"
    , default="{}/words.db".format(click.get_app_dir(app_name))
    , help="Set the path to the words database to use.")
@click.option("--form", "-f", default="{adverb} {verb}ing {adjective} {noun}", help="Set the format of the generated name. The format will be called with four named parameters: {adverb}, {adjective}, {noun}, and {verb}")
def name(number_of_names_wanted, db_path, form):
    """Generate a name from randomly chosen parts-of-speech.

    This tool generates a name by randomly selecting an adjective, adverb, verb,
    and noun, then printing them in the following order: \"adverb verb adjective
    noun\". E.g.: \"quickly fuming inverted car\". Such names are often highly
    memorable, and with a modest collection of words, we can generate a very
    large number of unique names. This means that these names can be used in
    place of serial numbers for such things as work tickets, task IDs, or bug
    numbers. It is to be hoped that we humans have a much easier time
    remembering them as well.
    """

    log = logging.getLogger(__name__)

    secho("Generating names", fg="yellow", bold=True)

    log.debug('(options (number-of-names-wanted {}) (db_path "{}))'.format(number_of_names_wanted, db_path))

    db = words.words.words(db_path)

    for i in range(number_of_names_wanted):
        click.echo(db.name(form=form))
    pass
