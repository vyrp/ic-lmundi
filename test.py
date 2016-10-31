import dev_appserver
import traceback
dev_appserver.fix_sys_path()

try:
    import main
    assert hasattr(main, "app"), "Module 'main' should have 'app' field"
except ImportError as ex:
    for line in traceback.format_exc().splitlines()[-3:]:
        print line.strip()
    print
    exit(1)
except AssertionError as ex:
    print ex
    print
    exit(1)
