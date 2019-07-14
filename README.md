>_Che Fá il mio Amato Pappá? io sto cosí bene, e tanto contenta che non posso se
>non ringraziare il sempre Caro mio Pappa che mi procuró un tanto bene da cui
>imploro la sua Benedizione, la sua Allegrina lo saluta di cuore._

>~[Allegra Byron](https://en.wikipedia.org/wiki/Allegra_Byron)

# Allegra

A TCP port based mystery

## The Story

Talk to Allegra and discover her secrets:

    telnet cosmic.voyage 1822

## Installation

Install the service:

    sudo make install

_The systemd service is designed to run as the unprivileged user 'allegra'. This user is created during the install process if it doesn't already exist on your system._

Start the service:

    sudo systemctl start allegra

## Removal

Uninstall the service:

    sudo make uninstall
