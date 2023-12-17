Main |:
    <w> "Write two numbers"
    <?> a
    <?> b
    Euclides a b
:|

Euclides a b |:
    while a != b |:
        if a > b |:
            a <- a - b
        :| else |:
            b <- b - a
        :|
    :|
    <w> "Their GCD is" a
:|
